from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Request, Response
from passlib.context import CryptContext
import jwt

from app.schemas.user import User, UserAdd, UserLogin, UserRequestAdd
from app.services.base import BaseService
from app.config import settings


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, password_hash) -> bool:
        return self.pwd_context.verify(plain_password, password_hash)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as e:
            raise e

    async def register_user(self, user_data: UserRequestAdd) -> User:
        password_hash = self.hash_password(user_data.password)
        new_user_data = UserAdd(
            username=user_data.username, email=user_data.email, password_hash=password_hash
        )
        new_user = await self.db.user.add(data=new_user_data)
        await self.db.commit()
        return new_user

    async def login_user(self, user_data: UserLogin, response: Response) -> str:
        user = await self.db.user.get_user_by_email(user_data.email)

        if not self.verify_password(user_data.password, user.password_hash):
            raise HTTPException(401, detail="Неправильный пароль")
        access_token = self.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token, httponly=True)
        return {"access_token": access_token}

    async def logout_user(self, request: Request, response: Response) -> None:
        if not request.cookies.get("access_token"):
            raise HTTPException(401, detail="Сессия недействительна")
        response.delete_cookie("access_token")
