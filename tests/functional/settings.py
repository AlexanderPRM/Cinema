from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    es_adress: str = Field("http:/127.0.0.1:9200", env="ELASTIC_ADRESS")
    es_id_field: str = Field("id")

    # В дальнейшем убрать! (Возможно пригодиться при разработке)
    # es_index_mapping: dict =

    redis_adress: str = Field("http:/127.0.0.1:6379", env="REDIS_ADRESS")
    service_url: str = Field("http:/127.0.0.1:8000", env="SERVICE_URL")

    class Config:
        case_sensitive = False
        env_file = "config_tests.env"


class FilmsSettings(BaseConfig):
    es_index: str = Field("movies")


class GenreSettings(BaseConfig):
    es_index: str = Field("genres")


class PersonSetting(BaseConfig):
    es_index: str = Field("persons")


films_settings = FilmsSettings()
genre_setting = GenreSettings()
person_settings = PersonSetting()
