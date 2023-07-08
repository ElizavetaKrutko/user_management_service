from fastapi import APIRouter, Depends, HTTPException, status

from app.db.dependencies.repository import setup_repository
from app.db.repositories.postgres_repo import PostgresRepository

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/signup")
async def signup(repo=Depends(setup_repository(PostgresRepository))):
    # NO AUTHORIZATION
    # Accepts the user’s login (username, email, phone_number) and password:
    # * username, email, phone_number -> MUST be uniq
    # Creates a user in DB.
    # Generates JWT (Access & Refresh tokens) as a response
    return "Not implemented"


@router.post("/login")
async def login(repo=Depends(setup_repository(PostgresRepository))):
    # NO AUTHORIZATION
    # Accepts the user’s login (username, email or phone number) and password, returns access and refresh tokens
    # Generates JWT (Access & Refresh tokens) as a response
    return "Not implemented"


@router.post("/refresh-token")
async def refresh_token(repo=Depends(setup_repository(PostgresRepository))):
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    # Accepts refresh token and returns new access and refresh tokens.
    # Old refresh token should be blacklisted using Redis
    return "Not implemented"


@router.post("/reset-password")
async def reset_password(repo=Depends(setup_repository(PostgresRepository))):
    # NO AUTHORIZATION
    # Accepts the user's email address and sends an email with a link to reset the password.
    # Another optional endpoint can be added to implement this logic
    return "Not implemented"
