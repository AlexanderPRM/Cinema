import datetime

from utils.connect import postgres_connection


class Extract:
    def __init__(self, psql_dsn, chunk_size, storage_state, logger) -> None:
        self.chunk_size = chunk_size
        self.state = storage_state
        self.dsn = psql_dsn
        self.logger = logger

    def extract(
        self,
        extract_timestamp: datetime.datetime,
        start_timestamp: datetime.datetime,
        exclude_ids: list,
    ):
        with postgres_connection(self.dsn) as pg_conn, pg_conn.cursor() as cursor:
            stmt = f"""
                    SELECT
                        p.id,
                        p.full_name,
                        string_agg(DISTINCT CASE WHEN pfw.role = 'director' THEN fw.title ELSE '' END, ',') AS director,
                        string_agg(DISTINCT CASE WHEN pfw.role = 'actor' THEN fw.title ELSE '' END, ',') AS actors,
                        string_agg(DISTINCT CASE WHEN pfw.role = 'writer' THEN fw.title ELSE '' END, ',') AS writers,
                        MAX(p.updated_at) AS last_modified
                    FROM
                        content.person p
                        LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
                        LEFT JOIN content.film_work fw ON pfw.film_work_id = fw.id
                    GROUP BY p.id
                    """
            if exclude_ids:
                stmt += f"""
                AND (p.id not in {tuple(exclude_ids)} OR
                  MAX(p.updated_at) > '{str(start_timestamp)}')
                """
            stmt += f"""
            HAVING MAX(p.updated_at) > '{str(extract_timestamp)}'
            ORDER BY MAX(p.updated_at) DESC;
            """
            cursor.execute(stmt)
            while True:
                rows = cursor.fetchmany(self.chunk_size)
                if not rows:
                    self.logger.info("Changes not found")
                    break
                self.logger.info(f"Extracted {len(rows)} lines")
                for data in rows:
                    ids_list = self.state.get_state("stopped_uuid")
                    ids_list.append(data["id"])
                    self.state.set_state("stopped_uuid", ids_list)
                yield rows
