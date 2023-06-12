from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    NOTF_PROJECT_NAME: str
    NOTF_PROJECT_VERSION: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


project_settings = ProjectSettings()
