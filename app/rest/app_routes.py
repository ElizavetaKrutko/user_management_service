from fastapi import APIRouter, Depends

from app.db.dependencies.repository import setup_repository
from app.db.repositories.postgres_repo import PostgresRepository

router = APIRouter(
    prefix="/api/v1",
    tags=["healthcheck"],
)


@router.get("/healthcheck")
async def healthcheck(repo=Depends(setup_repository(PostgresRepository))):
    return {"message": "Ready to work!"}
