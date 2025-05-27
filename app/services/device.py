from app.schemas.device import DeviceAddRequest, DeviceAdd
from app.services.base import BaseService


class DeviceService(BaseService):
    async def get_devices(self, user_id: int):
        return await self.db.device.get_filtered(user_id=user_id)
    
    async def add_device(self, data: DeviceAddRequest, user_id: int):
        device_data = DeviceAdd(**data.model_dump(), user_id=user_id)
        new_device = await self.db.device.add(data=device_data)
        await self.db.commit()
        return new_device


    