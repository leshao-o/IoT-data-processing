from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.schemas.user import User
from app.models import UserORM
from app.CRUD.base import BaseCRUD
from app.logger import logger


class UserCRUD(BaseCRUD):
    model = UserORM
    schema = User

    async def get_user_by_email(self, email: EmailStr) -> User:
        logger.info("Получение пользователя по email")
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
            logger.info("Пользователь получен успешно")
        except NoResultFound as e:
            logger.error("Пользователь не найден")
            raise e
        return model
