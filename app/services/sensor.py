from app.schemas.sensor import SensorAdd
from app.services.base import BaseService


class SensorService(BaseService):
    async def get_sensors(self, device_id: int):
        return await self.db.sensor.get_filtered(device_id=device_id)
    
    async def add_sensor(self, data: SensorAdd):
        new_sensor = await self.db.sensor.add(data)
        await self.db.commit()
        return new_sensor
