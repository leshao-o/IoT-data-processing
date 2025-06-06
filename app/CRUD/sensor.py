from sqlalchemy.orm import selectinload

from app.CRUD.base import BaseCRUD
from app.models import SensorORM
from app.schemas.sensor import Sensor


class SensorCRUD(BaseCRUD):
    model = SensorORM
    schema = Sensor
    load_options = [
        selectinload(SensorORM.data),
        selectinload(SensorORM.alerts),
        selectinload(SensorORM.device)
    ]
