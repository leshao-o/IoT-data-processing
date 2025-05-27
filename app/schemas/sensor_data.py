from pydantic import BaseModel
from datetime import datetime


class SensorDataAdd(BaseModel):
    sensor_id: int
    value: float


class SensorData(SensorDataAdd):
    id: int
    timestamp: datetime
    