from utils.connect import postgres_connection


class Extract:
    def __init__(self, psql_dsn, chunk_size, storage_state, logger) -> None:
        self.chunk_size = chunk_size
        self.state = storage_state
        self.dsn = psql_dsn
        self.logger = logger

    def extract(self):
        with postgres_connection(self.dsn) as pg_conn, pg_conn.cursor() as cursor:
            sql = f"""
                    SELECT
                        p.id,
                        p.full_name
                    FROM content.person p
                    """
            cursor.execute(sql)
            while True:
                rows = cursor.fetchmany(self.chunk_size)
                if not rows:
                    self.logger.info('Changes not found')
                    break
                self.logger.info(f'Extracted {len(rows)} lines')
                for data in rows:
                    ids_list = self.state.get_state("stopped_uuid")
                    ids_list.append(data['id'])
                    self.state.set_state("stopped_uuid", ids_list)
                yield rows
