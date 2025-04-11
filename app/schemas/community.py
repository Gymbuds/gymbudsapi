from pydantic import BaseModel
from typing import Optional
class CommunityCreate(BaseModel):
    name: str
    address: str
    latitude : float
    longitude : float
    


