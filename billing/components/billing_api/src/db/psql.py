from sqlalchemy.ext.asyncio import create_async_engine


class PostgreSQL:
    def __init__(self, conn_url, **kwargs) -> None:
        self.engine = create_async_engine(conn_url, kwargs)
