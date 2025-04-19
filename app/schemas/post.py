from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommunityPostCreate(BaseModel):
    community_id: int
    title: str
    content: str
    image_url: Optional[str] = None

class CommunityPostResponse(CommunityPostCreate):
    id: int
    user_id: int
    created_at: datetime

class CommunityPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None