from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1", tags=["user", "users"])


@router.get("/user/me")
async def get_me():
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    # Should GET the user by user_id from JWT (returns user info)
    return "Not implemented"


@router.patch("/user/me")
async def patch_me():
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    # Should PATCH the user info by user_id from JWT
    # Accepts new values for the fields to update and returns the updated user info
    return "Not implemented"


@router.delete("/user/me")
async def delete_me():
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    # Should DELETE the user (Deletes the user by id probably)
    return "Not implemented"


@router.get("/users")
async def get_users(
    page: int = 1,
    limit: int = 30,
    filter_by_name: str = "",
    sort_by: str = "id",
    order_by: str = "asc",
):
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    #                   Should check if the requester is (ADMIN) OR (MODERATOR of the group that the user belongs to)
    # Should GET the users
    # Returns a collection of users based on filtering and pagination parameters:
    # * Returns all users if requester is an ADMIN.
    # * Returns users related to the group if requester is a MODERATOR.
    return "Not implemented"


@router.get("/user/{user_id}")
async def get_user_by_id():
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    #                   Should check if the requester is (ADMIN) OR (MODERATOR of the group that the requested user belongs to)
    # Should GET the user
    # Returns the user info based on the user_id
    return "Not implemented"


@router.patch("/user/{user_id}")
async def update_user_by_id():
    # AUTHORIZATION:    JWT authentication (User ID is extracted from the JWT)
    #                   Should check if the requester is ADMIN
    # Should PATCH the user data
    # Accepts new values for the fields to update and returns the updated user info
    return "Not implemented"
