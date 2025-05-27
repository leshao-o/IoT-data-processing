from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.CRUD.base import BaseCRUD
from app.models import DeviceORM
from app.schemas.device import Device, DeviceWithRels
from app.logger import logger


class DeviceCRUD(BaseCRUD):
    model = DeviceORM
    schema = Device
    load_options = [
        selectinload(DeviceORM.sensors),
        selectinload(DeviceORM.commands)
    ]

    async def get_filtered(self, **filter_by) -> list[DeviceWithRels]:
        logger.info("Получение данных по фильтру")
        query = select(self.model).options(*self.load_options).filter_by(**filter_by)
        result = await self.session.execute(query)
        models = [
            DeviceWithRels.model_validate(one, from_attributes=True) for one in result.scalars().all()
        ]
        logger.info("Данные получены успешно")
        return models
