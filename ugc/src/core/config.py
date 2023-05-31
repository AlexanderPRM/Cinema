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

    class Config:
        case_sensitive = True
        env_file = "config.env"


class MongoCollectionsNames(BaseSettings):
    FILM_REVIEW_COLLECTION: str
    FILM_LIKES_COLLECTION: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


project_settings = UGCSettings()
collections_names = MongoCollectionsNames()
