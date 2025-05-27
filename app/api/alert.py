from fastapi import APIRouter

from app.services.alert import AlertService 
from app.dependencies import DBDep, UserIDDep
from app.schemas.alert import AlertAdd
from app.logger import logger


router = APIRouter(prefix="/alert", tags=["Предупреждения"])


@router.get("")
async def get_alerts(db: DBDep, user_id: UserIDDep, sensor_id: int):
    logger.info("Получение предупреждения")
    return await AlertService(db).get_alerts(sensor_id=sensor_id)


@router.post("")
async def add_alert(db: DBDep, alert_data: AlertAdd, user_id: UserIDDep):
    logger.info("Добавление нового предупреждения")
    return await AlertService(db).add_alert(alert_data=alert_data)
