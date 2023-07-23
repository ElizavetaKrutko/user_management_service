from fastapi import APIRouter, Depends, status

from app.dependencies.security import (get_user_from_access_token,
                                       get_user_from_refresh_token)
from app.dependencies.usecase_dependencies import get_auth_management_use_case
from app.rest.routes import schemas
from app.usecases.auth import AuthManagementUseCase

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post(
    "/signup",
    response_model=schemas.TokensResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    new_user_data: schemas.UserCreate,
    auth_use_case: AuthManagementUseCase = Depends(get_auth_management_use_case),
):
    # Creates a user in DB. Add token in a "whitelist" in Redis
    return await auth_use_case.create_user(new_user_data.to_entity())


@router.post("/login", response_model=schemas.TokensResponseSchema)
async def login(
    user_credentials: schemas.UserLogin,
    auth_use_case: AuthManagementUseCase = Depends(get_auth_management_use_case),
):
    # Accepts the user’s login (username, email or phone number) and password, returns access and refresh tokens
    return await auth_use_case.login_user(user_credentials.to_entity())


@router.post("/logout")
async def logout(
    auth_use_case: AuthManagementUseCase = Depends(get_auth_management_use_case),
    user_data: schemas.UserInfo = Depends(get_user_from_access_token),
):
    return await auth_use_case.logout_user(user_data.id)


@router.post("/refresh-token", response_model=schemas.TokensResponseSchema)
async def refresh_token(
    auth_use_case: AuthManagementUseCase = Depends(get_auth_management_use_case),
    user_data: schemas.UserInfo = Depends(get_user_from_refresh_token),
):
    # Accepts refresh token and returns new access and refresh tokens.
    # Old refresh token is blacklisted using Redis and check is tokens from response in blacklist

    return await auth_use_case.create_jwt_token(user_data.id)


@router.post("/request-password-reset")
async def reset_password(
    user_data: schemas.UserRequestResetPassword,
    auth_use_case: AuthManagementUseCase = Depends(get_auth_management_use_case),
):
    return await auth_use_case.send_reset_password_email(user_data.to_entity())


@router.post("/reset-password")
async def reset_password(
    user_data: schemas.UserResetPassword,
    token: str,
    auth_use_case: AuthManagementUseCase = Depends(get_auth_management_use_case),
):
    return await auth_use_case.update_password(user_data.to_entity(), token)
