from pydantic import BaseModel


class SensorAdd(BaseModel):
    name: str
    type: str
    device_id: int


class Sensor(SensorAdd):
    id: int
    