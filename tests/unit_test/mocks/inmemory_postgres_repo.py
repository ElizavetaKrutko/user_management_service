import uuid

from app.domain.user import Role, User
from app.ports.user_port import UserRepositoryPort


class InMemoryUserRepository(UserRepositoryPort):
    def __init__(self) -> None:
        self.users = [
            {
                "id": "991bbf56-cfec-45af-8f97-21c97ef4058e",
                "username": "nastya123",
                "hashed_password": "$2b$12$3gCXLZDiN7hR8WmCQcI6KePpeqUWIlnYbNKJwt8kCbNFr8Jm5WaDK",
                "phone_number": "+375293484455",
                "email": "nastya123.@gmail.com",
                "group_id": 1,
                "role": Role.ADMIN,
            },
            {
                "id": "32d8790f-bce9-430e-ad70-b8a410cd66e9",
                "username": "ekaterina123",
                "hashed_password": "$2b$12$3gCXLZDiN7hR8WmCQcI6KePpeqUWIlnYbNKJwt8kCbNFr8Jm5WaDK",
                "phone_number": "+375293484444",
                "email": "ekaterina123.@gmail.com",
                "group_id": 1,
                "role": Role.USER,
                "is_blocked": True,
            },
            {
                "id": "c43358e3-3846-45e6-9901-25e23fc836a7",
                "username": "anna123",
                "hashed_password": "$2b$12$3gCXLZDiN7hR8WmCQcI6KePpeqUWIlnYbNKJwt8kCbNFr8Jm5WaDK",
                "phone_number": "+375293484466",
                "email": "anna123.@gmail.com",
                "group_id": 2,
                "role": Role.USER,
            },
        ]

    async def create_user(self, user: User):
        return user

    async def get_user_by_id(self, user_id: uuid.UUID):
        for user in self.users:
            if user["id"] == user_id:
                return user

    async def get_user_by_login(self, username, email=None, phone_number=None):
        if email is None:
            email = username
        if phone_number is None:
            phone_number = username
        for user in self.users:
            if (
                user["username"] == username
                or user["email"] == email
                or user["phone_number"] == phone_number
            ):
                return User(**user)

    async def update_user_by_id(self, new_user_data: User, user_id: uuid.UUID):
        for user in self.users:
            if user["id"] == user_id:
                user = new_user_data.dict()
                return user

    async def delete_user(self, user_id: uuid.UUID):
        pass

    async def get_users_by_filters(self, users_filter, group_id=None):
        pass
