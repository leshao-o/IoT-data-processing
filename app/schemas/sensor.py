from pydantic import BaseModel


class Sensor(BaseModel):
    id: int
    name: str
    type: str
    device_id: int