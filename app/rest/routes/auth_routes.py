import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.db.dependencies.repository import setup_repository
from app.db.repositories.postgres_repo import PostgresRepository
from app.db.repositories.redis_repo import RedisRepository
from app.rest import schemas
from app.services import auth_service

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post(
    "/signup",
    response_model=schemas.TokensResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    new_user_data: schemas.UserCreate,
    db_repo: PostgresRepository = Depends(setup_repository(PostgresRepository)),
    redis_repo: RedisRepository = Depends(RedisRepository),
):
    # Creates a user in DB. Add token in a "whitelist" in Redis
    user_data = await auth_service.create_user(db_repo, new_user_data)
    return await auth_service.create_jwt_token(redis_repo, user_data.id)


@router.post("/login", response_model=schemas.TokensResponseSchema)
async def login(
    user_credentials: schemas.UserLogin,
    db_repo: PostgresRepository = Depends(setup_repository(PostgresRepository)),
    redis_repo: RedisRepository = Depends(RedisRepository),
):
    # Accepts the user’s login (username, email or phone number) and password, returns access and refresh tokens
    user_data = await auth_service.login_user(db_repo, user_credentials)
    return await auth_service.create_jwt_token(redis_repo, user_data.id)


@router.post("/logout")
async def logout(
    db_repo: PostgresRepository = Depends(setup_repository(PostgresRepository)),
    redis_repo: RedisRepository = Depends(RedisRepository),
    user_data: schemas.UserBaseRead = Depends(auth_service.get_user_from_jwt),
):
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    # Logouts the user from the system
    # Old refresh token should be blacklisted using Redis
    logging.error(user_data.dict())
    await auth_service.logout_user(redis_repo, user_data.id)
    return "The user logged out"


@router.post("/refresh-token", response_model=schemas.TokensResponseSchema)
async def refresh_token(
    db_repo=Depends(setup_repository(PostgresRepository)),
    redis_repo: RedisRepository = Depends(RedisRepository),
    user_data: schemas.UserBaseRead = Depends(auth_service.get_user_from_jwt),
):
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    # Accepts refresh token and returns new access and refresh tokens.
    # Old refresh token should be blacklisted using Redis and check is tokens from responce in blacklist

    return await auth_service.create_jwt_token(redis_repo, user_data.id)


@router.post("/reset-password")
async def reset_password(db_repo=Depends(setup_repository(PostgresRepository))):
    # NO AUTHORIZATION
    # Accepts the user's email address and sends an email with a link to reset the password.
    # Another optional endpoint can be added to implement this logic - ?
    return "Not implemented"
