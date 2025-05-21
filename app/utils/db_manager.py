from app.CRUD.alert import AlertCRUD
from app.CRUD.base import BaseCRUD
from app.CRUD.device import DeviceCRUD
from app.CRUD.device_command import DeviceCommandCRUD
from app.CRUD.sensor import SensorCRUD
from app.CRUD.sensor_data import SensorDataCRUD
from app.CRUD.user import UserCRUD


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.base = BaseCRUD(self.session)
        self.alert = AlertCRUD(self.session)
        self.device_command = DeviceCommandCRUD(self.session)
        self.device = DeviceCRUD(self.session)
        self.sensor_data = SensorDataCRUD(self.session)
        self.sensor = SensorCRUD(self.session)
        self.user = UserCRUD(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
