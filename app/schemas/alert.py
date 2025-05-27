from pydantic import BaseModel
from datetime import datetime


class Alert(BaseModel):
    id: int
    sensor_id: str
    alert_type: str
    description: str
    created_at: datetime
