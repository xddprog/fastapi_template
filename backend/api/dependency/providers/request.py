from typing import AsyncIterable
from dishka import FromDishka, Provider, Scope, provide
from dishka.integrations.fastapi import inject
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core import repositories, services
from backend.core.dto.user_dto import BaseUserModel
from backend.infrastructure.database.connection.postgres_connection import DatabaseConnection


class RequestProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self, db_connection: DatabaseConnection) -> AsyncIterable[AsyncSession]:
        session = await db_connection.get_session()
        try:
            yield session
        finally:
            await session.close()

    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, session: AsyncSession) -> services.AuthService:
        return services.AuthService(repository=repositories.UserRepository(session=session))
    
    @provide(scope=Scope.REQUEST)
    def get_user_service(self, session: AsyncSession) -> services.UserService:    
        return services.UserService(repository=repositories.UserRepository(session=session))

@inject
async def get_current_user_dependency(
    auth_service: FromDishka[services.AuthService], 
    request: Request
) -> BaseUserModel:
    token = request.cookies.get('access_token')
    data = await auth_service.verify_token(token)
    return await auth_service.check_user_exist(data)
