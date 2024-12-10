from pydantic import BaseModel
from pydantic.v1 import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class DatabaseConfig(BaseConfig):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str


class JWTConfig(BaseConfig):
    JWT_SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_TIME: int


class S3StorageConfig(BaseConfig):
    BUCKET_NAME: str
    ACCESS_KEY_ID: str
    SECRET_ACCESS_KEY: str
    REGION: str
    ENDPOINT_URL: str


class RedisConfig(BaseConfig):
    REDIS_HOST: str
    REDIS_PORT: int
