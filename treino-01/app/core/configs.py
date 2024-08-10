from typing import Any

from pydantic.v1 import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://lordpoxta:274661@localhost:5432/tasks'
    DB_BASE_URL: Any = declarative_base()

    class Config:
        case_sensitive = True


settings: Settings = Settings()
