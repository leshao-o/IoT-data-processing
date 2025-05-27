from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserAdd(BaseModel):
    username: str
    email: str
    password_hash: str


class User(UserAdd):
    id: int
    created_at: datetime


class UserRequestAdd(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str
