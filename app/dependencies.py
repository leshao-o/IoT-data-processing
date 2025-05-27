from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, Request

from app.database import async_session_maker
from app.schemas.user import User
from app.services.auth import AuthService
from app.utils.db_manager import DBManager
from app.logger import logger


async def get_db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


def get_token(request: Request) -> str:
    logger.info("Получение токена")
    token = request.cookies.get("access_token", None)
    if not token:
        logger.error("Токен не найден")
        raise HTTPException(401, detail="Ошибка токена доступа")
    return token


def get_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except Exception as e:
        logger.error("Ошибка токена")
        raise e
    return data.get("user_id")


UserIDDep = Annotated[User, Depends(get_user_id)]
