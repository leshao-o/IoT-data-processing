from pydantic import BaseModel
from datetime import datetime


class SensorDataAdd(BaseModel):
    sensor_id: str
    type: str
    value: float


class SensorData(SensorDataAdd):
    id: int
    timestamp: datetime


class Alert(BaseModel):
    id: int
    sensor_id: str
    alert_type: str
    description: str
    created_at: datetime


class DeviceCommandAdd(BaseModel):
    device_id: str
    command: str


class DeviceCommand(DeviceCommandAdd):
    id: int
    status: str
    timestamp: datetime


class Device(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    created_at: datetime


class Sensor(BaseModel):
    id: int
    name: str
    type: str
    device_id: int


class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime
