from pydantic import BaseModel
from datetime import datetime
class MessageOut(BaseModel):
    type: str
    content: str | None = None
    image_url:str | None = None
    chat_id:int 
    sender_id: int
    timestamp: datetime