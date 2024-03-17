from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings, extra="ignore"):
    API_HOST: str
    API_PORT: int
    DEVELOPMENT_MODE: bool
    DATABASE_URL: str
    SSL_KEY_PATH: str
    SSL_CERT_PATH: str
    FRONTEND_URL: str

    LOG_LEVEL: str
    LOG_FILE: str
    CONSOLE_ENABLED: bool

    MARIADB_HOST: str
    MARIADB_USER: str
    MARIADB_PASSWORD: str
    MARIADB_DATABASE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_config() -> Config:
    return Config()
