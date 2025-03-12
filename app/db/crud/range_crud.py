from app.db.models.avalrange import AvailabilityRange
from sqlalchemy.orm import Session
from datetime import time

def create_avail_range(db: Session, user_id: int, start_time: time, end_time: time, day_week: str):
    """
    Create a new availability range for a user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.
        start_time (time): The start time of the availability range.
        end_time (time): The end time of the availability range.
        day_week (str): The day of the week for the availability range.

    Returns:
        AvailabilityRange: The created availability range.
    """
    db_aval_range = AvailabilityRange(user_id=user_id, day_of_week=day_week, start_time=start_time, end_time=end_time)
    db.add(db_aval_range)
    db.commit()
    db.refresh(db_aval_range)
    return db_aval_range

def get_availability_ranges_user(db: Session, user_id: int):
    """
    Get all availability ranges for a user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        list: A list of availability ranges for the user.
    """
    availability_ranges = db.query(AvailabilityRange).filter(AvailabilityRange.user_id == user_id).all()
    return availability_ranges