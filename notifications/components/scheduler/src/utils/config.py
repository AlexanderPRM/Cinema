from pydantic import BaseSettings, Field


class PostgreSettings(BaseSettings):
    NOTF_POSTGRES_DB: str
    NOTF_POSTGRES_HOST: str
    NOTF_POSTGRES_PORT: str
    NOTF_POSTGRES_USER: str
    NOTF_POSTGRES_PASSWORD: str
    TEMPLATE_TABLE: str = Field("templates")

    class Config:
        case_sensitive = True
        env_file = "notf.env"


class SchedulerSettings(BaseSettings):
    RECOMMENDATIONS: str = Field("recommendations")
    NEW_EPISODES: str = Field("new_episodes")
    PERSON_LIKES: str = Field("person_likes")
    RECOMMENDATIONS_TIMEOUT: int = Field(720)
    NEW_EPISODES_TIMEOUT: int = Field(360)
    PERSON_LIKES_TIMEOUT: int = Field(360)
    NOTIFICATION_SERVICE_URL: str = Field("http://notification_api:8001/api/v1/notify/send/")


pg_settings = PostgreSettings()
scheduler_settings = SchedulerSettings()
