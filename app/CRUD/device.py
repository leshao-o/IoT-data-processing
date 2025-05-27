from app.CRUD.base import BaseCRUD
from app.models import DeviceORM
from app.schemas.device import Device


class DeviceCRUD(BaseCRUD):
    model = DeviceORM
    schema = Device
