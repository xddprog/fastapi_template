from backend.core.repositories.user_repository import UserRepository
from backend.core.services.base import BaseDbModelService
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.user_errors import UserNotFound


class UserService(BaseDbModelService[UserRepository]):
    pass
