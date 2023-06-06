from fastapi import Query
from pydantic import BaseSettings


class UGCSettings(BaseSettings):
    UGC_PROJECT_NAME: str
    UGC_PROJECT_VERSION: str
    MONGO_DB: str
    JWT_SECRET: str
    MONGOS1_HOST: str
    MONGOS1_PORT: str
    MONGOS2_HOST: str
    MONGOS2_PORT: str
    LOGSTASH_HOST: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class MongoCollectionsNames(BaseSettings):
    FILM_REVIEW_COLLECTION: str
    BOOKMARK_COLLECTION: str
    FILM_REVIEW_RATE_COLLECTION: str
    FILM_RATING_COLLECTION: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


class CommonQueryParams:
    def __init__(
        self,
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1, le=50),
    ):
        self.page_number = page_number
        self.page_size = page_size


project_settings = UGCSettings()
collections_names = MongoCollectionsNames()
