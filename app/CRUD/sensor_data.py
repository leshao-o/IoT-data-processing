from app.CRUD.base import BaseCRUD
from app.models import SensorDataORM
from app.schemas import SensorData


class SensorDataCRUD(BaseCRUD):
    model = SensorDataORM
    schema = SensorData
