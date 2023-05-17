import time

import vertica_python

from logger import logger
from settings import vertica_config

class VerticaWorker:
    def make_connection(self):
        connection_info = {
            "host": vertica_config.vertica_host,
            "port": vertica_config.vertica_port,
            "user": vertica_config.vertica_user,
            "password": vertica_config.vertica_password,
            "database": vertica_config.vertica_db,
            "autocommit": vertica_config.vertica_autocommit,
        }
        connection = vertica_python.connect(**connection_info)
        return connection

    def create_table(self, connection):
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS views (
            id IDENTITY,
            user_id VARCHAR(256) NOT NULL,
            movie_id VARCHAR(256) NOT NULL,
            timestamp INTEGER NOT NULL
        );
        """)

    def load_data(self, connection, file_path):
        cursor = connection.cursor()
        cursor.execute("""
        COPY views (user_id, movie_id, timestamp)
        FROM '{}'
        DELIMITER ','
        ENCLOSED BY '"'
        SKIP 1
        ;
        """.format(file_path))

    def count_rows(self, connection):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT COUNT(*) FROM views;
        """)
        row = cursor.fetchone()
        return row[0]

    def truncate_table(self, connection):
        cursor = connection.cursor()
        cursor.execute("""
        TRUNCATE TABLE views;
        """)


if __name__ == "__main__":
    vertica_test = VerticaWorker()
    connection = vertica_test.make_connection()
    vertica_test.create_table(connection)
    data_list = [
        ('/home/dbadmin/data/films_progress_50.csv', 50),
        ('/home/dbadmin/data/films_progress_1_000.csv', 1000),
        ('/home/dbadmin/data/films_progress_10_000.csv', 10000),
        ('/home/dbadmin/data/films_progress_100_000.csv', 100000),
        ('/home/dbadmin/data/films_progress_1_000_000.csv', 1000000),
        ('/home/dbadmin/data/films_progress_10_000_000.csv', 10000000),
    ]
    for data in data_list:
        print("Loading {} in progress...".format(data[1]))
        current = time.time()
        vertica_test.load_data(connection, data[0])
        end = time.time() - current
        logger.info(f"{format(data[1], ',d')} loaded in {end:.2f} seconds")

        row_count = vertica_test.count_rows(connection)
        assert row_count == data[1]

        vertica_test.truncate_table(connection)
    print("Done")
    connection.close()
