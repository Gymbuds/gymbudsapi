from pydantic import BaseModel
from datetime import datetime

class MatchResultCreate(BaseModel):
    matched_user_id: int

class MatchResultResponse(BaseModel):
    id: int
    user_id1: int
    user_id2: int
    matched_at: datetime