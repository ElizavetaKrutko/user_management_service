from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from app.dependencies.security import get_user_from_access_token
from app.dependencies.usecase_dependencies import get_user_management_use_case
from app.rest.routes import schemas
from app.rest.routes.filters import UsersFilter
from app.usecases.user import UserUseCase

router = APIRouter(prefix="/api/v1", tags=["user", "users"])


@router.get("/user/me", response_model=schemas.UserPublicInfo)
async def get_me(user_data: schemas.UserInfo = Depends(get_user_from_access_token)):
    return user_data


@router.patch("/user/me", response_model=schemas.UserPublicInfo)
async def patch_me(
    modified_user_data: schemas.UserUpdate,
    user_use_case: UserUseCase = Depends(get_user_management_use_case),
    user_data: schemas.UserInfo = Depends(get_user_from_access_token),
):
    return await user_use_case.patch_user(modified_user_data.to_entity(), user_data.id)


@router.delete("/user/me")
async def delete_me(
    user_use_case: UserUseCase = Depends(get_user_management_use_case),
    user_data: schemas.UserInfo = Depends(get_user_from_access_token),
):
    deleted_user_id = await user_use_case.delete_user(user_data.id)
    return f"User with id= {deleted_user_id} was successfully deleted"


@router.get("/user/{user_id}", response_model=schemas.UserPublicInfo)
async def get_another_user_by_id(
    user_id: UUID,
    user_use_case: UserUseCase = Depends(get_user_management_use_case),
    user_data: schemas.UserInfo = Depends(get_user_from_access_token),
):
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    # Should check if the requester is (ADMIN) OR (MODERATOR of the group that the requested user belongs to)
    # Should GET the user
    # Returns the user info based on the user_id
    return await user_use_case.get_another_user_by_id(user_id, user_data)


@router.patch("/user/{user_id}")
async def edit_another_user_by_id(
    modified_user_data: schemas.UserUpdate,
    user_id: UUID,
    user_use_case: UserUseCase = Depends(get_user_management_use_case),
    user_data: schemas.UserInfo = Depends(get_user_from_access_token),
):
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    # Should check if the requester is ADMIN
    # Should PATCH the user data
    # Accepts new values for the fields to update and returns the updated user info
    return await user_use_case.edit_another_user_by_id(
        modified_user_data.to_entity(), user_id, user_data
    )


@router.get("/users", response_model=Page[schemas.UserPublicInfo])
async def get_users_with_queries(
    user_use_case: UserUseCase = Depends(get_user_management_use_case),
    user_data: schemas.UserInfo = Depends(get_user_from_access_token),
    users_filter: UsersFilter = FilterDepends(UsersFilter),
):
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    #                   Should check if the requester is (ADMIN) OR (MODERATOR of the group that the user belongs to)
    # Should GET the users
    # Returns a collection of users based on filtering and pagination parameters:
    # page: int = 1, limit: int = 30, filter_by_name: str = "", sort_by: str = "id", order_by: str = "asc"
    # * Returns all users if requester is an ADMIN.
    # * Returns users related to the group if requester is a MODERATOR.
    return await user_use_case.get_users_with_queries(user_data, users_filter)
