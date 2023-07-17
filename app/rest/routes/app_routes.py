from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/v1",
    tags=["healthcheck"],
)


@router.get("/healthcheck")
async def healthcheck():
    return {"message": "Ready to work!"}
