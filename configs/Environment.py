from functools import lru_cache

from pydantic_settings import BaseSettings


class EnvironmentSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str

    #DELETE if need
    MINIO_BASE_BUCKET: str
    MINIO_HOST: str
    MINIO_SECRET: str
    MINIO_ACCESS: str

    DEBUG: bool

    class Config:
        env_file = "configs/.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables() -> EnvironmentSettings:
    return EnvironmentSettings()
