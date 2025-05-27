from pydantic import BaseModel
from datetime import datetime


class DeviceCommandAdd(BaseModel):
    device_id: int
    command: str


class DeviceCommand(DeviceCommandAdd):
    id: int
    status: str
    timestamp: datetime
