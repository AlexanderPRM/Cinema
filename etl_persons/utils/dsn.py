import dotenv
from pydantic import BaseSettings, Field

dotenv.load_dotenv()


class Dsn(BaseSettings):
    dbname: str = Field("movies_database", env="POSTGRES_DB")
    user: str = Field("app", env="POSTGRES_USER")
    password: str = Field("app", env="POSTGRES_PASSWORD")
    host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    port: str = Field(5432, env="POSTGRES_PORT")


class Config(BaseSettings):
    batch_size: int = Field(50, env="BATCH_SIZE")
    etl_timeout: float = Field(60.0, env="ETL_TIMEOUT")
    es_host: str = Field("localhost", env="ELASTIC_HOST")
    es_port: int = Field("9200", env="ELASTIC_PORT")
    dsn: dict = Dsn().dict()
