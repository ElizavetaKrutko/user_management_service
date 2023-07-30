import uuid
from abc import ABC

from app.common import utils
from app.common.config import logger
from app.domain.user import User
from app.ports.user_port import UserRepositoryPort


class InMemoryUserRepository(UserRepositoryPort):
    def __init__(self) -> None:
        self.users = {}

    async def create_user(self, user: User):
        hashed_password = utils.get_hashed_password(user.password)
        del user.password
        user.hashed_password = hashed_password
        user.id = uuid.uuid4()
        self.users[user.id] = user
        return User

    async def get_user_by_id(self, user_id: uuid.UUID):
        current_user = []
        for user in self.users.values():
            if user.id == user_id:
                current_user.append(user)
        return current_user

    async def get_user_by_login(self, username, email=None, phone_number=None):
        current_user = []
        if email is None:
            email = username
        if phone_number is None:
            phone_number = username
        for user in self.users.values():
            if (
                user.username == username
                or user.email == email
                or user.phone_number == phone_number
            ):
                current_user.append(user)
        return current_user

    async def update_user_by_id(self, new_user_data: User, user_id: uuid.UUID):
        return new_user_data

    async def delete_user(self, user_id: uuid.UUID):
        pass

    async def get_users_by_filters(self, users_filter, group_id=None):
        pass
