from pydantic import BaseSettings, Field


class CronSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ADMIN_ROLE: str
    UGC_URL: str = Field("http://ugc2:8000/api/v1/films/")
    SITE_LINK: str = Field("localhost")

    class Config:
        case_sensitive = True
        env_file = "notf.env"


class PostgreSQLSettings(BaseSettings):
    NOTF_POSTGRES_DB: str
    NOTF_POSTGRES_HOST: str
    NOTF_POSTGRES_PORT: str
    NOTF_POSTGRES_USER: str
    NOTF_POSTGRES_PASSWORD: str
    LIKES_TEMPLATE_ID: str = Field("5a4fd7c0-8cef-44f5-a16d-0f78f72b0900")
    USERS_CATEGORY_FOR_LIKE_NOTIFICATIONS: str = Field("efbae92b-e130-4715-8665-ca78f6a34eb6")
    TASKS_TABLE: str = Field("tasks")

    class Config:
        case_sensitive = True
        env_file = "notf.env"


postgres_settings = PostgreSQLSettings()
cron_setting = CronSettings()
