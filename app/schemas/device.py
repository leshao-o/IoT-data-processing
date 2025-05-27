from pydantic import BaseModel
from datetime import datetime

from app.schemas.device_command import DeviceCommand
from app.schemas.sensor import Sensor


class DeviceAddRequest(BaseModel):
    name: str
    description: str


class DeviceAdd(BaseModel):
    name: str
    user_id: int
    description: str


class Device(DeviceAdd):
    id: int
    created_at: datetime


class DeviceWithRels(Device):
    sensors: list[Sensor]
    commands: list[DeviceCommand]
