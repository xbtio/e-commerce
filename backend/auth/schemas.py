import uuid

from fastapi_users import schemas
import datetime


class UserRead(schemas.BaseUser[int]):
    name: str
    created_date: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    name: str


class UserUpdate(schemas.BaseUserUpdate):
    name: str
