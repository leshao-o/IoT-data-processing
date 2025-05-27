from app.schemas.sensor_data import SensorDataAdd
from app.services.base import BaseService


class SensorDataService(BaseService):
    async def get_sensor_data(self, sensor_id: int):
        return await self.db.sensor_data.get_filtered(sensor_id=sensor_id)
    
    async def add_sensor_data(self, data: SensorDataAdd):
        new_data = await self.db.sensor_data.add(data)
        await self.db.commit()
        return new_data
