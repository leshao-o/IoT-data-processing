from sqlalchemy.orm import selectinload
from app.CRUD.base import BaseCRUD
from app.models import DeviceCommandORM
from app.schemas.device_command import DeviceCommand


class DeviceCommandCRUD(BaseCRUD):
    model = DeviceCommandORM
    schema = DeviceCommand
    load_options = [selectinload(DeviceCommandORM.device)]
