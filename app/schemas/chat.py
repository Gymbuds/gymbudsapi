from pydantic import BaseModel
from datetime import datetime
class MessageOut(BaseModel):
    type: str
    content: str
    chat_id:int
    sender_id: int
    timestamp: datetime