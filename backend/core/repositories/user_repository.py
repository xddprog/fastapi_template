from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.repositories.base import SqlAlchemyRepository
from backend.infrastructure.database.models.auth_methods import AuthMethod
from backend.infrastructure.database.models.user import User


class UserRepository(SqlAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def register_external_service_user(self, username: str, email: str, **kwargs):
        user = User(username=username, email=email)
        auth_method = AuthMethod(user=user, **kwargs)

        self.session.add_all([user, auth_method])
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_emails(self, emails: list[str], only_ids: bool = False):
        query = select(self.model if not only_ids else self.model.id).where(self.model.email.in_(emails))
        users = await self.session.execute(query)
        return users.scalars().all()
    
    async def get_by_ids(self, ids: list[int]):
        query = select(self.model).where(self.model.id.in_(ids))
        users = await self.session.execute(query)
        return users.scalars().all()