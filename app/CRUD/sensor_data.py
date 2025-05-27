from sqlalchemy.orm import selectinload
from app.CRUD.base import BaseCRUD
from app.models import SensorDataORM
from app.schemas.sensor_data import SensorData


class SensorDataCRUD(BaseCRUD):
    model = SensorDataORM
    schema = SensorData
    load_options = [selectinload(SensorDataORM.sensor)]
