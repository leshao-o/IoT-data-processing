from fastapi import APIRouter

from app.services.device import DeviceService
from app.dependencies import DBDep, UserIDDep
from app.schemas.device import DeviceAddRequest
from app.logger import logger


router = APIRouter(prefix="/device", tags=["Устройства"])


@router.get("")
async def get_devices(db: DBDep, user_id: UserIDDep):
    logger.info("Получение устройства")
    return await DeviceService(db).get_devices(user_id=user_id)


@router.post("")
async def add_device(db: DBDep, device_data: DeviceAddRequest, user_id: UserIDDep):
    logger.info("Добавление нового устройства")
    return await DeviceService(db).add_device(data=device_data, user_id=user_id)
