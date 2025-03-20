from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class LogMethod(str, Enum):
    MANUAL = "MANUAL"
    VOICE = "VOICE"

class MoodType(str, Enum):
    ENERGIZED = "ENERGIZED"
    TIRED = "TIRED"
    MOTIVATED = "MOTIVATED"
    STRESSED = "STRESSED"
    NEUTRAL = "NEUTRAL"

class ExerciseDetail(BaseModel):
    exercise_name: str
    sets: int
    reps: int
    weight: Optional[float] = None

class ExerciseDetailResponse(ExerciseDetail):
    exercise_id: int

class WorkoutLogBase(BaseModel):
    title: str
    type: LogMethod
    exercise_details: List[ExerciseDetail]
    notes: Optional[str] = None
    duration_minutes: int
    mood: MoodType

class WorkoutLogCreate(WorkoutLogBase):
    pass

class WorkoutLogUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[LogMethod] = None
    exercise_details: Optional[List[ExerciseDetailResponse]] = None 
    delete_exercises: Optional[List[int]] = None  # IDs of exercises to delete
    notes: Optional[str] = None
    duration_minutes: Optional[int] = None
    mood: Optional[MoodType] = None

class WorkoutLog(WorkoutLogBase):
    id: int
    user_id: int
    exercise_details: List[ExerciseDetailResponse]
    date: datetime