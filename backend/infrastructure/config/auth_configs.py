from environs import Env
from pydantic import BaseModel


env = Env()
env.read_env()


class JwtConfig(BaseModel):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_TIME: int
    JWT_REFRESH_TOKEN_TIME: int


JWT_CONFIG = JwtConfig(
    **{field: env.str(field) for field in JwtConfig.model_fields}
)
