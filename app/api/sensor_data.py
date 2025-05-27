from fastapi import APIRouter

from app.dependencies import DBDep, UserIDDep
from app.schemas.sensor_data import SensorDataAdd
from app.services.sensor_data import SensorDataService

router = APIRouter(prefix="/sensor_data", tags=["Информация с датчиков"])


@router.get("")
async def get_sensor_data(db: DBDep, sensor_id: int, user_id: UserIDDep):
    data = await SensorDataService(db).get_sensor_data(sensor_id=sensor_id)
    return data


@router.post("")
async def add_sensor_data(db: DBDep, sensor_data: SensorDataAdd, user_id: UserIDDep):
    new_data = await SensorDataService(db).add_sensor_data(sensor_data)
    return new_data
