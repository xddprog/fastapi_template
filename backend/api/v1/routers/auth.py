from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response

from backend.api.dependency.providers.request import get_current_user_dependency
from backend.core import cache, clients, services
from backend.core.dto.auth_dto import ExternalServiceUserData, LoginForm, RegisterForm
from backend.core.dto.user_dto import BaseUserModel
from backend.utils.enums import AuthServices
from backend.utils.auth_requests import AuthRequests


router = APIRouter()


async def set_cookie_tokens(access_token: str, refresh_token: str, response: Response):
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)


@router.get("/current_user")
@inject
async def get_current_user(
    request: Request,
    current_user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
) -> BaseUserModel:
    return current_user


@router.post("/check-exist")
@inject
async def check_user_in_app(
    userForm: RegisterForm,
    auth_service: FromDishka[services.AuthService],
    two_factor_service: FromDishka[services.TwoFactorAuthService],
    smtp_clients: FromDishka[clients.SMTPClients],
) -> None:
    await auth_service.check_user_in_app(userForm)
    code = await two_factor_service.generate_code(userForm.username)
    await smtp_clients.send_verification_code(userForm.email, code, userForm.username)


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
async def logout_user(
    response: Response,
    request: Request,
) -> dict[str, str]:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"detail": "Вы вышли из аккаунта"}


@router.post("/register", status_code=201)
@inject
async def register_user(
    form: RegisterForm,
    code: str,
    response: Response,
    auth_service: FromDishka[services.AuthService],
    two_factor_service: FromDishka[services.TwoFactorAuthService]
) -> BaseUserModel:
    await auth_service.check_user_in_app(form)
    # await two_factor_service.check_code(form.username, code)
    new_user, access_token, refresh_token = await auth_service.register_user(form)
    await set_cookie_tokens(access_token, refresh_token, response)
    return new_user


@router.post("/vk")
@inject
async def login_with_vk(
    code: str, 
    auth_service: FromDishka[services.AuthService],
    auth_requests: FromDishka[AuthRequests],
    response: Response
):
    token, user_id = await auth_requests.get_vk_access_token(code)
    user = await auth_requests.get_vk_user(token, user_id)

    user = await auth_service.auth_extarnal_service_user(
        ExternalServiceUserData(
            username=f"{user["first_name"]} {user['last_name']}",
            external_id=user["id"],
            service=AuthServices.VK.value,
        )
    )
    access_token = await auth_service.create_access_token(user.username)
    refresh_token = await auth_service.create_refresh_token(user.username)

    await set_cookie_tokens(access_token, refresh_token, response)
    return user


@router.post("/yandex")
@inject
async def login_with_yandex(
    access_token: str, 
    auth_service: FromDishka[services.AuthService],
    auth_requests: FromDishka[AuthRequests],
    response: Response
):
    user = await auth_requests.get_yandex_user(access_token)
    user = await auth_service.auth_extarnal_service_user(
        ExternalServiceUserData(
            username=user["display_name"],
            email=user["default_email"],
            external_id=user["id"],
            service=AuthServices.YANDEX.value,
        )
    )

    access_token = await auth_service.create_access_token(user.username)
    refresh_token = await auth_service.create_refresh_token(user.username)
    await set_cookie_tokens(access_token, refresh_token, response)
    return user
