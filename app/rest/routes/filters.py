from datetime import datetime
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.adapters.orm_engines.models import UserORM


class UsersFilter(Filter):
    name__in: Optional[list[str]] = Field(alias="names")
    surname__in: Optional[list[str]] = Field(alias="surnames")
    username__in: Optional[list[str]] = Field(alias="usernames")
    phone_number__in: Optional[list[str]] = Field(alias="phone_numbers")
    email__in: Optional[list[str]] = Field(alias="emails")
    is_blocked__in: Optional[list[bool]] = Field(alias="blocked")
    created_at__gte: Optional[datetime] = Field(alias="created_at")
    group_id__in: Optional[list[int]] = Field(alias="groups")
    order_by: Optional[list[str]] = Field(alias="order_by")

    class Constants(Filter.Constants):
        model = UserORM

    class Config:
        allow_population_by_field_name = True
