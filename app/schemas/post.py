from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CommunityPostCreate(BaseModel):
    community_id: int
    title: str
    content: str
    image_url: Optional[str] = None

class CommunityPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class PostCommentCreate(BaseModel):
    content: str

class PostCommentResponse(PostCommentCreate):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

class CommunityPostResponse(CommunityPostCreate):
    id: int
    user_id: int
    created_at: datetime
    like_count: Optional[int] = 0
    comments: Optional[List[PostCommentResponse]] = []