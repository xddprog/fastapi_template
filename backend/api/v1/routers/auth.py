from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Request, Response

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import services
from backend.core.dto.auth_dto import LoginForm, RegisterForm
from backend.core.dto.user_dto import BaseUserModel


router = APIRouter()


async def set_cookie_tokens(access_token: str, refresh_token: str, response: Response):
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)


@router.get("/current_user")
@inject
async def get_current_user(
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
) -> BaseUserModel:
    return current_user


@router.post("/login")
@inject
async def login_user(
    form: LoginForm,
    response: Response,
    auth_service: FromDishka[services.AuthService]
) -> BaseUserModel:
    user, access_token, refresh_token = await auth_service.login_user(form)
    await set_cookie_tokens(access_token, refresh_token, response)
    return user


@router.post("/refresh")
@inject
async def refresh_token(
    request: Request, 
    response: Response,
    auth_service: FromDishka[services.AuthService]
):
    refresh_token = request.cookies.get("refresh_token")
    email = await auth_service.verify_token(refresh_token)
    access_token = await auth_service.create_access_token(email)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    

@router.delete("/logout")
@inject
async def logout_user(response: Response) -> dict[str, str]:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"detail": "Вы вышли из аккаунта"}


@router.post("/register", status_code=201)
@inject
async def register_user(
    form: RegisterForm,
    response: Response,
    auth_service: FromDishka[services.AuthService],
) -> BaseUserModel:
    new_user, access_token, refresh_token = await auth_service.register_user(form)
    await set_cookie_tokens(access_token, refresh_token, response)
    return new_user
