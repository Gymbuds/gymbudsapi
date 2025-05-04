from pydantic import BaseModel
from datetime import datetime

from enum import Enum

class GenderPref(str,Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    BOTH = "BOTH"
    
class Status(str,Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
class MatchResultCreate(BaseModel):
    matched_user_id: int

class MatchResultResponse(BaseModel):
    id: int
    user_id1: int
    user_id2: int
    matched_at: datetime

class MatchPreferenceUpdate(BaseModel):
    gender: GenderPref | None = None
    start_weight: int | None = None 
    end_weight: int | None = None
    max_location_distance_miles: int | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    profile_picture: str | None = None
    preferred_workout_goals: str | None = None
    age: int | None = None 
    skill_level: str | None = None 
    weight: int | None = None
    gender: str | None = None
class CandidateCreate(BaseModel):
    user_id: int
    candidate_user_id: int
    score: int
class StatusUpdate(BaseModel):
    match_candidate_id: int
    status: Status
