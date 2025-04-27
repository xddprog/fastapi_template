from fastapi import APIRouter, Depends, Request
from backend.api.dependency.providers.request import get_current_user_dependency
from backend.api.v1.routers.auth import router as auth_router
from backend.api.v1.routers.user import router as users_router


v1_router = APIRouter(prefix='/v1')
PROTECTED = Depends(get_current_user_dependency)

v1_router.include_router(auth_router, tags=['auth'], prefix='/auth')
v1_router.include_router(users_router, tags=['users'], prefix='/user', dependencies=[PROTECTED])