from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal


class Settings(BaseSettings):
    app_name: str = "Zen Stock Screener API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    api_v1_prefix: str = "/api/v1"
    allowed_origins: list[str] = ["http://localhost:3000", "http://frontend:3000"]

    redis_url: str = "redis://redis:6379/0"
    redis_ttl_seconds: int = 300

    data_source: Literal["mock", "real"] = "mock"
    alpha_vantage_key: str = ""
    finnhub_key: str = ""
    polygon_key: str = ""

    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
