from functools import lru_cache
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    API_URL: str
    API_PORT: int
    DEVELOPMENT_MODE: bool
    DATABASE_URL: str
    SSL_KEY_PATH: str
    SSL_CERT_PATH: str
    FRONTEND_URL: str

    LOG_LEVEL: str
    LOG_FILE: str
    CONSOLE_ENABLED: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_config() -> Config:
    return Config()
