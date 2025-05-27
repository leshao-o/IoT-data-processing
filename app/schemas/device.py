from pydantic import BaseModel
from datetime import datetime


class Device(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    created_at: datetime
    