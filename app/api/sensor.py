from fastapi import APIRouter

from app.dependencies import DBDep, UserIDDep
from app.schemas.sensor import SensorAdd
from app.services.sensor import SensorService

router = APIRouter(prefix="/sensors", tags=["Датчики"])


@router.get("")
async def get_sensors(db: DBDep, device_id: int, user_id: UserIDDep):
    sensors = await SensorService(db).get_sensors(device_id=device_id)
    return sensors


@router.post("")
async def add_sensor(db: DBDep, sensor_data: SensorAdd, user_id: UserIDDep):
    new_sensor = await SensorService(db).add_sensor(sensor_data)
    return new_sensor
