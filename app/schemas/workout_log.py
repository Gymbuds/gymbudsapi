from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WorkoutLogBase(BaseModel):
    exercise: str
    sets: int
    reps: int
    weight: Optional[float] = None
    mood: str

class WorkoutLogCreate(WorkoutLogBase):
    pass

class WorkoutLog(WorkoutLogBase):
    id: int
    created_at: datetime