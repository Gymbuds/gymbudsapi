from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class AIAdviceType(str, Enum):
    WORKOUT_ADVICE = "WORKOUT_ADVICE"
    WORKOUT_OPTIMIZATION = "WORKOUT_OPTIMIZATION"
    RECOVERY_ANALYSIS = "RECOVERY_ANALYSIS"
    PERFORMANCE_TRENDS = "PERFORMANCE_TRENDS"
    MUSCLE_BALANCE = "MUSCLE_BALANCE"
    GOAL_ALIGNMENT = "GOAL_ALIGNMENT"

class AIAdviceBase(BaseModel):
    advice_type: AIAdviceType
    health_data:bool

class AIAdviceResponse(BaseModel):
    id: int
    advice_type: AIAdviceType
    ai_feedback: str
    user_id: int
    created_at: datetime
    workout_earliest_date: datetime | None = None
    workout_latest_date: datetime | None = None
    contains_health_data:bool