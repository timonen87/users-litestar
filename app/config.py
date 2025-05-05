import os
from litestar import Litestar

from litestar.openapi import OpenAPIConfig
from enum import Enum
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MODE: str = "development"
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    APP_HOST : str = os.getenv("APP_HOST", "localhost")
    APP_PORT : str = os.getenv("APP_PORT", "8000")
    APP_DOMAIN: str = os.getenv("APP_DOMAIN", "8000")
    

    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "postgres")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "users_litestar")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


settings = Settings()

