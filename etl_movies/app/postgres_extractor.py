import logging

from app.quiries import SQL_QUERY
from psycopg2.extensions import connection as psql_connection
from utils.models import Movie
from utils.state import State


class PostgtresExtractor:
    def __init__(self, conn: psql_connection, storage: State, limit: int) -> None:
        self.conn = conn
        self.cur = conn.cursor()
        self.storage = storage
        self.limit = limit
        self.last_updated = self.storage.get_state("last_updated")

    def extract(self):
        if (
            self.storage.get_state("last_updated_fw")
            and self.storage.get_state("last_updated_p")
            and self.storage.get_state("last_updated_g")
        ):
            self.cur.execute(
                SQL_QUERY
                % (
                    """WHERE fw.updated_at > '%s'
                    OR g.updated_at > '%s'
                    OR p.updated_at > '%s'"""
                    % (
                        self.storage.get_state("last_updated_fw"),
                        self.storage.get_state("last_updated_g"),
                        self.storage.get_state("last_updated_p"),
                    ),
                    self.limit,
                )
            )
        else:
            self.cur.execute(SQL_QUERY % ("", self.limit))
        result = []
        response = self.cur.fetchall()
        if response:
            max_p = max(response[0][9])
            max_g = max(response[0][10])
        for movie in response:
            if movie[7]:
                max_p = max(max_p, max(movie[10]))
            if movie[8]:
                max_g = max(max_g, max(movie[9]))
            result.append(
                Movie(
                    id=movie[0],
                    title=movie[1],
                    description=movie[2],
                    rating=movie[3],
                    type=movie[4],
                    created_at=movie[5],
                    updated_at=movie[6],
                    persons=movie[7],
                    genres=movie[8],
                )
            )
        try:
            self.storage.set_state("last_updated_fw", result[-1].updated_at)
            state_persons = self.storage.get_state("last_updated_p")
            if state_persons:
                if max_p > state_persons:
                    self.storage.set_state("last_updated_p", max_p)
            else:
                self.storage.set_state("last_updated_p", max_p)
            state_genre = self.storage.get_state("last_updated_g")
            if state_genre:
                if max_g > state_genre:
                    self.storage.set_state("last_updated_g", max_g)
            else:
                self.storage.set_state("last_updated_g", max_g)
        except IndexError:
            logging.error("IndexError: Записей больше нет.")
        return result
