import datetime
import json
import logging
from collections.abc import Generator  # используется для тайпингов
from functools import wraps
from time import sleep
from typing import Optional, Tuple

import psycopg2
import psycopg2.extras
import requests
from backoff import backoff
from config import Settings
from psycopg2.extras import DictCursor, DictRow
from pydantic import BaseModel
from state_script import *

logging.basicConfig(level=logging.DEBUG)


# функция для отправки cURL requests
def elasticsearch_curl(uri='', json_body='', verb='get'):
    headers = {
        'Content-Type': 'application/json',
    }
    try:
        if verb.lower() == 'get':
            resp = requests.get(uri, headers=headers, data=json_body)
        elif verb.lower() == 'post':
            resp = requests.post(uri, headers=headers, data=json_body)
        elif verb.lower() == 'put':
            resp = requests.put(uri, headers=headers, data=json_body)
        elif verb.lower() == 'delete':
            resp = requests.delete(uri, headers=headers, data=json_body)

        try:
            resp_text = json.loads(resp.text)
        except BaseException:
            resp_text = resp.text

    except Exception as error:
        logging.debug('\nelasticsearch_curl() error:', error)
        resp_text = error

    logging.debug('resp_text:', resp_text)
    return resp_text


def coroutine(func):
    @wraps(func)
    def inner(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Generator:
        fn: Generator = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


def create_index():
    with open('./etl/settings_index.json') as settings_index:
        settings = json.load(settings_index)

    elasticsearch_curl(
        uri=Settings().dict().get('URI_LOAD_DATA'),
        verb='put',
        json_body=json.dumps(settings),
    )


class TransformData_to_correct_json(BaseModel):
    id: str
    imdb_rating: Optional[float] = 0.0
    genre: Tuple = []
    title: str = ''
    description: Optional[str] = ''


def load_from_postgres(batch: Generator, cursor_pg, table):
    state = State(JsonFileStorage('.'))
    try:
        time = datetime.datetime.fromisoformat(state.get_state(table))
    except TypeError:
        time = datetime.datetime(
            1000, 1, 16, 20, 14, 9, 222485, tzinfo=datetime.timezone.utc)
    # ПОЛУЧАЕМ ВСЮ ИНФУ ДЛЯ ЗАПИСИ В ЭЛАСТИК
    last_modified = datetime.datetime(1000, 1, 16)
    if table == 'content.film_work':
        cursor_pg.execute(
            f"""
                    SELECT
                       fw.id,
                       fw.title,
                       fw.description,
                       fw.rating as imdb_rating,
                       fw.modified,
                       COALESCE (
                           json_agg(
                               DISTINCT jsonb_build_object(
                                   'person_role', pfw.role,
                                   'person_id', p.id,
                                   'person_name', p.full_name
                               )
                           ) FILTER (WHERE p.id is not null),
                           '[]'
                       ) as persons,
                       array_agg(DISTINCT g.name) as genre
                    FROM content.film_work fw
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                    LEFT JOIN content.person p ON p.id = pfw.person_id
                    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                    LEFT JOIN content.genre g ON g.id = gfw.genre_id
                    WHERE fw.modified > '{time}'
                    GROUP BY fw.id
                    ORDER BY fw.modified
                    ;
                    """
        )
    elif table == 'content.person' or table == 'content.genre':
        cursor_pg.execute(
            f"""
                    SELECT id, modified
                    FROM {table}
                    WHERE modified > '{time}'
                    ORDER BY modified
                    ;
                    """
        )
        film_list = []
        while True:
            person_entries = cursor_pg.fetchmany(1000)
            if len(person_entries) == 0:
                break
            entries_list = []
            for entry in person_entries:
                entries_list.append(entry[0])
                last_modif = entry[1]
            last_modified = last_modif
            if table == 'content.person':
                m2m_table = 'content.person_film_work'
                short_m2m_table = 'pfw'
                id_column = 'person_id'
            elif table == 'content.genre':
                m2m_table = 'content.genre_film_work'
                short_m2m_table = 'gfw'
                id_column = 'genre_id'
            ids = "','".join(entries_list)
            # За всеми фильмами и сериалами, в которых приняли участие выбранные
            # люди/которые соответствуют выбранным жанрам.
            cursor_pg.execute(
                f"""
                    SELECT fw.id, fw.modified
                    FROM content.film_work fw
                    LEFT JOIN {m2m_table} {short_m2m_table} ON {short_m2m_table}.film_work_id = fw.id
                    WHERE {short_m2m_table}.{id_column} IN ('{ids}')
                    ORDER BY fw.modified
                    ;
                    """
            )
            films = cursor_pg.fetchall()
            for film in films:
                film_list.append(film[0])

        if film_list != []:
            # ПОЛУЧАЕМ ВСЮ ИНФУ ДЛЯ ЗАПИСИ В ЭЛАСТИК
            ids = "','".join(film_list)
            cursor_pg.execute(
                f"""
                        SELECT
                           fw.id,
                           fw.title,
                           fw.description,
                           fw.rating as imdb_rating,
                           COALESCE (
                               json_agg(
                                   DISTINCT jsonb_build_object(
                                       'person_role', pfw.role,
                                       'person_id', p.id,
                                       'person_name', p.full_name
                                   )
                               ) FILTER (WHERE p.id is not null),
                               '[]'
                           ) as persons,
                           array_agg(DISTINCT g.name) as genre
                        FROM content.film_work fw
                        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                        LEFT JOIN content.person p ON p.id = pfw.person_id
                        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                        LEFT JOIN content.genre g ON g.id = gfw.genre_id
                        WHERE fw.id IN ('{ids}')
                        GROUP BY fw.id
                        ORDER BY fw.modified
                        ;
                        """
            )
    while True:
        size = 500
        try:
            entries = cursor_pg.fetchmany(size)
        except BaseException:
            break
        if len(entries) == 0 or entries is None:
            # дата изменения последней отправленной в ETL записи, отличная от
            # 1000-01-16 00:00:00 - гарантия того, что изменения были
            if str(last_modified) != '1000-01-16 00:00:00':
                state.set_state(table, str(last_modified))
                if table == 'content.film_work' and state.get_state('is_first_loop') is None:
                    # Меняем поле последнего изменения в состоянии для двух других таблиц, что
                    # бы после самого первого цикла отправки данных в etl, не проделывать эту
                    # операцию еще дважды
                    state.set_state('content.person', str(last_modified))
                    state.set_state('content.genre', str(last_modified))
                    # Параметр is_first_loop в состоянии нужен для индентификации самого
                    # первого цикла
                    state.set_state('is_first_loop', 'False')
            break
        else:
            if table == 'content.film_work':
                last_modified = entries[-1][4]
            data_list = entries
            batch.send(data_list)


@coroutine
def transform(batch: Generator) -> Generator[None, DictRow, None]:
    while data_list := (yield):
        json_body = ''
        for data in data_list:
            data_etl_json = dict(TransformData_to_correct_json(**dict(data)))
            data_dict = dict(data)
            data_etl_json['director'] = []
            data_etl_json['actors_names'] = []
            data_etl_json['writers_names'] = []
            data_etl_json['actors'] = []
            data_etl_json['writers'] = []
            for person in data_dict.get('persons'):
                if person.get('person_role') == 'director':
                    data_etl_json['director'].append(person.get('person_name'))
                elif person.get('person_role') == 'actor':
                    data_etl_json['actors_names'].append(
                        person.get('person_name'))
                    data_etl_json['actors'].append(
                        {
                            'id': person.get('person_id'),
                            'name': person.get('person_name'),
                        }
                    )
                elif person.get('person_role') == 'writer':
                    data_etl_json['writers_names'].append(
                        person.get('person_name'))
                    data_etl_json['writers'].append(
                        {
                            'id': person.get('person_id'),
                            'name': person.get('person_name'),
                        }
                    )
            index = {
                'index': {
                    '_index': 'movies',
                    '_id': data_etl_json.get('id'),
                }
            }
            json_body += f'\n{json.dumps(index)}\n{json.dumps(data_etl_json)}\n'
        batch.send(json_body)


@coroutine
def load_to_etl():
    while json_body := (yield):
        state = State(JsonFileStorage('.'))
        # Создаем индекс, если еще не создан
        if state.get_state('index') is None:
            create_index()
            state.set_state('index', 'True')
        # Отправляем данны в ETL
        elasticsearch_curl(
            uri=Settings().dict().get('URI'),
            verb='post',
            json_body=json_body,
        )


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=1)
def connect_to_database():
    dsl = {
        'dbname': Settings().dict().get('DB_NAME'),
        'user': Settings().dict().get('DB_USER'),
        'password': Settings().dict().get('DB_PASSWORD'),
        'host': Settings().dict().get('HOST'),
        'port': 5432,
    }
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        cursor_pg = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            while True:
                tables = [
                    'content.film_work',
                    'content.person',
                    'content.genre',
                ]
                for table in tables:
                    unloads = load_to_etl()
                    multiplication = transform(unloads)
                    load_from_postgres(multiplication, cursor_pg, table)
                    sleep(5)

        finally:
            cursor_pg.close()
            pg_conn.close()


if __name__ == '__main__':
    connect_to_database()
