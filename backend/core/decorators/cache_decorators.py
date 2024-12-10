from functools import wraps
import json
from typing import Callable
from backend.services.auth_service import AuthService

from backend.core.redis_cache import RedisCache


class CacheUser(RedisCache):
    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> str:
            auth_service: AuthService = kwargs.get("auth_service")
            email = await auth_service.verify_token(
                kwargs.get("token")
            )
            user = await self.get_item(email)
            if user:
                return user.decode()
            
            result = await func(*args, **kwargs)
            await self.set_item(email, (await auth_service.get_user_by_email(email)).id)
            return result

        return wrapper
    