import json
import logging
from collections.abc import Generator  # используется для тайпингов
from functools import wraps

import requests
from config import settings as env_settings
from state_script import *

logging.basicConfig(level=logging.DEBUG)


def coroutine(func):
    @wraps(func)
    def inner(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Generator:
        fn: Generator = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


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


def create_index():
    with open('settings_index.json', mode='r') as settings_index:
        settings = json.load(settings_index)

    elasticsearch_curl(
        uri=env_settings.URI_LOAD_DATA,
        verb='put',
        json_body=json.dumps(settings),
    )


@coroutine
def load_to_etl():
    while json_body := (yield):
        state = State(JsonFileStorage('.'))
        # Создаем индекс, если еще не создан
        if state.get_state('index') is None:
            create_index()
            state.set_state('index', 'True')
        # Отправляем данны в ETL
        print(json_body)
        elasticsearch_curl(
            uri=env_settings.URI,
            verb='post',
            json_body=json_body,
        )
