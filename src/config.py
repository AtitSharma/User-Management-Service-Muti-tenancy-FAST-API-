from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(verbose=True)


class Settings(BaseSettings):

    ALGORITHM: str
    UMS_SERVER_PORT: str
    EUREKA_SERVER_URL: str
    ORIGINS: str
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URL: str
    EUREKA_SERVER_UMS_NAME: str
    SENTRY_DSN: str
    AUTH_SERVER_REGISTER_URL : str
    SCHEMAS : str
    DEFAULT_SCHEMA : str
    AUTH_REDIS_HOST : str
    AUTH_REDIS_PORT : str
    AUTH_DB_PASSWORD : str
    class Config:
        env_file = SettingsConfigDict(env_file=".env")


settings = Settings()
