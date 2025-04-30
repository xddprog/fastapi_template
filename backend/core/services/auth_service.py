from datetime import datetime, timedelta

from jwt import InvalidTokenError, encode, decode
from passlib.context import CryptContext

from backend.core.dto.auth_dto import LoginForm, RegisterForm
from backend.core.dto.user_dto import BaseUserModel
from backend.core.repositories.user_repository import UserRepository
from backend.infrastructure.config.auth_configs import JWT_CONFIG
from backend.infrastructure.database.models.user import User
from backend.infrastructure.errors.auth_errors import InvalidLoginData, InvalidToken, UserAlreadyNotRegister, UserAlreadyRegister


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.repository.get_by_attribute("username", username)
        return None if not user else user[0]
    
    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.repository.get_by_attribute("email", email)
        return None if not user else user[0]
    
    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.context.verify(password, hashed_password)

    async def authenticate_user(self, form: LoginForm | RegisterForm, is_external: bool = False) -> User:
        if is_external:
            user = await self.get_user_by_username(form.username)
        else:
            user = await self.get_user_by_email(form.email)
        if not user and is_external:
            return False
        if not user:
            raise UserAlreadyNotRegister
        if not is_external and not await self.verify_password(form.password, user.password):
            raise InvalidLoginData
        return BaseUserModel.model_validate(user, from_attributes=True)

    async def create_access_token(self, username: str) -> str:
        expire = datetime.now() + timedelta(minutes=JWT_CONFIG.JWT_ACCESS_TOKEN_TIME)
        data = {"exp": expire, "sub": username}
        token = encode(
            data,
            JWT_CONFIG.JWT_SECRET, 
            algorithm=JWT_CONFIG.JWT_ALGORITHM
        )
        return token
    
    async def create_refresh_token(self, username: str ):
        expire = datetime.now() + timedelta(days=JWT_CONFIG.JWT_REFRESH_TOKEN_TIME)
        data = {"exp": expire, "sub": username}
        return encode(
            data, 
            JWT_CONFIG.JWT_SECRET, 
            algorithm=JWT_CONFIG.JWT_ALGORITHM
        )

    async def verify_token(self, token: str) -> str:
        if not token:
            raise InvalidToken
        try:
            payload = decode(
                token,
                JWT_CONFIG.JWT_SECRET,
                algorithms=[JWT_CONFIG.JWT_ALGORITHM],
            )
            username = payload.get("sub")
            if not username or not await self.get_user_by_username(username):
                raise InvalidToken
            return username
        except (InvalidTokenError, AttributeError) as e:
            raise InvalidToken

    async def check_user_exist(self, username: str) -> BaseUserModel:
        user = await self.get_user_by_username(username)
        if user is None:
            raise InvalidToken
        return BaseUserModel.model_validate(user, from_attributes=True)

    async def register_user(self, form: RegisterForm) -> BaseUserModel:
        user = await self.get_user_by_email(form.email)
        if user:
            raise UserAlreadyRegister

        form.password = self.context.hash(form.password)
        new_user = await self.repository.add_item(**form.model_dump())
        access_token = await self.create_access_token(new_user.username)
        refresh_token = await self.create_refresh_token(new_user.username)
        return BaseUserModel.model_validate(new_user, from_attributes=True), access_token, refresh_token
    
    async def login_user(self, form: LoginForm) -> BaseUserModel:
        user = await self.authenticate_user(form)
        access_token = await self.create_access_token(user.username)
        refresh_token = await self.create_refresh_token(user.username)
        return user, access_token, refresh_token