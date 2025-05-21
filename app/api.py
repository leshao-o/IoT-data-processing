from fastapi import APIRouter

from app.dependencies import DBDep
from app.schemas import SensorData, SensorDataAdd
from app.CRUD.sensor_data import SensorDataCRUD
# from app.tasks import process_sensor_data

router = APIRouter(prefix="/api")


@router.post("/sensor-data")
async def add_sensor_data(data: SensorDataAdd):
    # process_sensor_data.delay(data.dict())
    return {"message": "Данные отправлены на обработку"}


@router.get("/sensor-data", response_model=list[SensorData])
async def read_sensor_data(db: DBDep):
    return await db.sensor_data.get_all()


# @router.get("/alerts", response_model=list[Alert]) 
# async def read_alerts(db: DBDep, limit: int = 10):
#     return crud.get_alerts(db, limit)


# @router.post("/device-command")
# async def send_command(command: DeviceCommandAdd):
#     # Здесь можно реализовать логику отправки команды (через очередь или заглушку)
#     return {"message": f"Команда '{command.command}' отправлена устройству {command.device_id}"}
