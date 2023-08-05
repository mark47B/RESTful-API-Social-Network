from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    PRJ_NAME: str
    PRJ_VERSION: str
    PRJ_DEBUG_ENVIRONMENT: bool

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB_NAME: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_USER: str
    POSTGRES_CONNECTION_STR: str

    REDIS_HOSTS: str
    REDIS_PORT: str
    REDIS_PASSWORD: SecretStr

    REDIS_COMMANDER_PORT: str

    class Config:
        env_file = "config/debug.env"
        env_file_encoding = "utf-8"


config = Settings()
