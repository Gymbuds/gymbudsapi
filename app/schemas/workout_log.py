from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class LogMethod(str, Enum):
    voice = "Voice"
    manual = "Manual"

class MoodType(str, Enum):
    energized = "Energized"
    tired = "Tired"
    motivated = "Motivated"
    stressed = "Stressed"
    neutral = "Neutral"

class ExerciseDetail(BaseModel):
    exercise: str
    sets: int
    reps: int
    weight: Optional[float] = None

class WorkoutLogBase(BaseModel):
    user_id: int
    title: str
    type: LogMethod
    exercise_details: List[ExerciseDetail]
    notes: Optional[str] = None
    duration_minutes: int
    mood: MoodType

class WorkoutLogCreate(WorkoutLogBase):
    pass

class WorkoutLog(WorkoutLogBase):
    id: int
    date: datetime