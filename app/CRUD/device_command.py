from app.CRUD.base import BaseCRUD
from app.models import DeviceCommandORM
from app.schemas import DeviceCommand


class DeviceCommandCRUD(BaseCRUD):
    model = DeviceCommandORM
    schema = DeviceCommand
