from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from tortoise import Tortoise

from backend.core.config import DatabaseConfig
from backend.database.models.base import Base

class DatabaseConnection:
    def __init__(self):
        self.__config = DatabaseConfig()
        self.__engine = create_async_engine(
            url=f"postgresql+asyncpg://{self.__config.DB_USER}:{self.__config.DB_PASS}"
            f"@{self.__config.DB_HOST}:{self.__config.DB_PORT}/{self.__config.DB_NAME}",
            poolclass=NullPool,
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(bind=self.__engine)

    async def __call__(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return self
