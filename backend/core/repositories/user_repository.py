from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.user import User


class UserRepository(SqlAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
