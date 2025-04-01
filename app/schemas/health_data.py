from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthDataCreate(BaseModel):
    steps: int
    calories_burnt: float
    avg_heart_rate: Optional[int] = None
    sleep_duration: Optional[float] = None
    active_mins: int

class HealthDataResponse(HealthDataCreate):
    id: int
    user_id: int
    date: datetime