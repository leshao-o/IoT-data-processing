from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.schemas.device import Device


class UserAdd(BaseModel):
    username: str
    email: str
    password_hash: str


class User(UserAdd):
    id: int
    created_at: datetime
    devices: list[Device]


class UserRequestAdd(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
