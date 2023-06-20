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
    RECOMMENDATIONS_TIMEOUT: int = Field(3600)
    NEW_EPISODES_TIMEOUT: int = Field(600)
    PERSON_LIKES_TIMEOUT: int = Field(180)


pg_settings = PostgreSettings()
scheduler_settings = SchedulerSettings()