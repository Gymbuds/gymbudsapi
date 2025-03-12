from app.db.models.avalrange import AvailabilityRange
from sqlalchemy.orm import Session
from datetime import time

def createavalRange(db:Session,user_id:int,start_time:time,end_time:time,day_week:str):
    db_aval_range = AvailabilityRange(user_id=user_id, day_of_week =day_week,start_time=start_time,end_time=end_time)
    db.add(db_aval_range)
    db.commit()
    db.refresh(db_aval_range)
    return db_aval_range

def get_availability_ranges_for_user(db: Session, user_id: int):
    availability_ranges = db.query(AvailabilityRange).filter(AvailabilityRange.user_id == user_id).all()
    return availability_ranges