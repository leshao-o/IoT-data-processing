from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, IntegrityError, ProgrammingError

from app.logger import logger


class BaseCRUD:
    model = None
    schema: BaseModel = None
    load_options = []

    def __init__(self, session):
        self.session = session

    # Метод для добавления данных в базу
    async def add(self, data: BaseModel) -> BaseModel:
        logger.info("Добавление данных в базу")
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
            logger.info("Данные добавлены успешно")
        except IntegrityError as e:
            logger.error("Ошибка добавления данных в базу")
            raise e
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model
    
    # Метод для добавления сразу нескольких строк данных в базу
    async def add_many(self, data: list[BaseModel]) -> list[BaseModel]:
        logger.info("Добавление нескольких строк данных в базу")
        stmt = insert(self.model).values([item.model_dump() for item in data])
        try:
            await self.session.execute(stmt)
            logger.info("Данные добавлены успешно")
        except IntegrityError as e:
            logger.error("Ошибка добавления данных")
            raise e

    # Метод для получения всех данных из таблицы
    async def get_all(self) -> list[BaseModel]:
        logger.info("Получение всех данных из таблицы")
        query = select(self.model).options(*self.load_options)
        result = await self.session.execute(query)
        models = [
            self.schema.model_validate(one, from_attributes=True)
            for one in result.scalars().all()
        ]
        logger.info("Данные получены успешно")
        return models

    # Метод для получения данных по ID
    async def get_by_id(self, id: int) -> BaseModel:
        logger.info("Получение данных по ID")
        query = select(self.model).options(*self.load_options).filter(self.model.id == id)
        result = await self.session.execute(query)
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        logger.info("Данные получены успешно")
        return model

    # Метод для получения данных по фильтру
    async def get_filtered(self, **filter_by) -> list[BaseModel]:
        logger.info("Получение данных по фильтру")
        query = select(self.model).options(*self.load_options).filter_by(**filter_by)
        result = await self.session.execute(query)
        models = [
            self.schema.model_validate(one, from_attributes=True) for one in result.scalars().all()
        ]
        logger.info("Данные получены успешно")
        return models

    # Метод для изменения данных, которые передали
    async def update(self, data: BaseModel, **filter_by) -> BaseModel:
        logger.info("Изменение данных")
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        try:
            result = await self.session.execute(stmt)
            logger.info("Данные изменены успешно")
        except (IntegrityError, ProgrammingError) as e:
            logger.error("Ошибка изменения данных")
            raise e

        try:
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        except NoResultFound as e:
            logger.error("Ошибка получения данных")
            raise e

        return model

    # Метод для удаления данных по заданным фильтрам
    async def delete(self, **filter_by) -> BaseModel:
        logger.info("Удаление данных")
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
            logger.info("Данные удалены успешно")
        except NoResultFound as e:
            logger.error("Ошибка удаления данных")
            raise e
        return model
