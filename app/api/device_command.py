from fastapi import APIRouter

from app.dependencies import DBDep, UserIDDep
from app.schemas.device_command import DeviceCommandAdd
from app.services.device_command import DeviceCommandService

router = APIRouter(prefix="/device_commands", tags=["Команды устройств"])


@router.get("")
async def get_device_commands(db: DBDep, device_id: int, user_id: UserIDDep):
    commands = await DeviceCommandService(db).get_device_commands(device_id=device_id)
    return commands


@router.post("")
async def add_device_command(db: DBDep, command_data: DeviceCommandAdd, user_id: UserIDDep):
    new_command = await DeviceCommandService(db).add_device_command(command_data)
    return new_command
