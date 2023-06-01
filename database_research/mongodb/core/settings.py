from pydantic import BaseModel, Field


class MongoConfig(BaseModel):
    host_1: str = Field(env="MONGO_HOST_1", default="mongos1")
    host_2: str = Field(env="MONGO_HOST_2", default="mongos2")
    port: str = Field(env="MONGO_PORT", default="27017")
    db_name: str = Field(env="MONGO_DB_NAME", default="test_db")
    db_collection: str = Field(env="MONGO_DB_COLLECTION", default="collection_likes")

    class Config:
        env_file = "config.env"


class CoreSettings(BaseModel):
    film_ids_filename: str = Field(env="FILM_IDS_FILENAME", default="film_ids")
    user_ids_filename: str = Field(env="USER_IDS_FILENAME", default="user_ids")
    film_count: int = Field(env="FILM_COUNT", default=100000)
    user_count: int = Field(env="USER_COUNT", default=1000000)
    min_liked_films: int = Field(env="MIN_LIKED_FILMS", default=2)
    max_liked_films: int = Field(env="MAX_LIKED_FILMS", default=6)
    batch_size: int = Field(env="BATCH_SIZE", default=10000)
    liked_min: int = Field(env="LIKED_MIN", default=1)


mongo_config = MongoConfig()
core_settings = CoreSettings()
