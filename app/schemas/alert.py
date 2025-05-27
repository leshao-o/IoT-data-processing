from pydantic import BaseModel
from datetime import datetime


class AlertAdd(BaseModel):
    sensor_id: int
    alert_type: str
    description: str


class Alert(AlertAdd):
    id: int
    created_at: datetime