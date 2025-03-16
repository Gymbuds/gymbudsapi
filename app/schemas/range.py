from pydantic import BaseModel
from datetime import time
class AvalRangeCreate(BaseModel):
    day_of_week : str
    start_time: time
    end_time: time
class AvalRangeDelete(BaseModel):
    id: int