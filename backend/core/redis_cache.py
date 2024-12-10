from typing import Any

from redis import Redis

from backend.core.config import RedisConfig


class RedisCache:
    def __init__(self) -> None:
        self.__config = RedisConfig()
        self.__redis: Redis = Redis(
            host=self.__config.REDIS_HOST, 
            port=self.__config.REDIS_PORT
        )

    async def set_item(self, key: str, value: Any) -> None:
        self.__redis.set(key, value)

    async def get_item(self, key: str) -> Any:
        return self.__redis.get(key)

    async def delete_item(self, key: str) -> None:
        self.__redis.delete(key)

    async def __call__(self):
        self.__redis.flushdb()
        return self
