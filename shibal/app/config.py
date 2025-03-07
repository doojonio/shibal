from pydantic import HttpUrl, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ASYNC_PG_DSN: PostgresDsn
    PG_DSN: PostgresDsn
    REDIS_DSN: RedisDsn
    CELERY_DSN: RedisDsn
    TG_BOT_TOKEN: str
    DRIVE_URL: HttpUrl


settings = Settings()
