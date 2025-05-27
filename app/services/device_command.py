from app.schemas.device_command import DeviceCommandAdd, DeviceCommand
from app.services.base import BaseService


class DeviceCommandService(BaseService):
    async def get_device_commands(self, device_id: int):
        return await self.db.device_command.get_filtered(device_id=device_id)
    
    async def add_device_command(self, data: DeviceCommandAdd):
        new_command = await self.db.device_command.add(data)
        await self.db.commit()
        return new_command
