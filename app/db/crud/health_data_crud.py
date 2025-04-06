from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import HTTPException
from datetime import datetime, timezone
from app.db.models.health_data import HealthData
from app.schemas.health_data import HealthDataCreate, HealthDataResponse
from datetime import timedelta,datetime
#Create a new health data entry
def create_health_data(db: Session, user_id: int, health_data: HealthDataCreate) -> HealthData:
    db_health = HealthData(
        user_id=user_id, 
        steps=health_data.steps,
        calories_burnt=health_data.calories_burnt,
        avg_heart_rate=health_data.avg_heart_rate,
        sleep_duration=health_data.sleep_duration,
        active_mins=health_data.active_mins,
        date=datetime.now(timezone.utc)  # Ensure correct date storage
    )
    db.add(db_health)
    db.commit()
    db.refresh(db_health)
    return db_health

def get_health_data_by_date(db: Session, user_id: int, date_str: str) -> HealthData:
    parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    health_data = db.query(HealthData).filter(
        HealthData.user_id == user_id,
        func.date(HealthData.date) == parsed_date
    ).first()

    if not health_data:
        raise HTTPException(status_code=404, detail="No health data found for this date")

    return health_data

def update_health_data(db: Session, health_id: int, user_id: int, health_data: HealthDataCreate) -> HealthDataResponse:
    health_entry = db.query(HealthData).filter(
        HealthData.id == health_id, HealthData.user_id == user_id
    ).first()

    if not health_entry:
        raise HTTPException(status_code=404, detail="Health data not found")

    # Update only the fields provided
    for key, value in health_data.dict(exclude_unset=True).items():
        setattr(health_entry, key, value)

    db.commit()
    db.refresh(health_entry)

    return health_entry
def get_health_data_by_user_latest(db:Session,user_id:int,latest_amt_days:int):
    date_threshold = datetime.now() - timedelta(days=latest_amt_days) # calculate how far back we need to go for users workouts
    health_datas = db.query(HealthData).filter(HealthData.user_id == user_id,HealthData.date > date_threshold).all()
    # earliest_date = db.query(HealthData).filter(
    #     HealthData.user_id == user_id,
    #     HealthData.date > date_threshold
    # ).order_by(HealthData.date).first().date
    return health_datas
def get_all_health_data_by_id(db:Session,user_id:int):
    health_datas = db.query(HealthData).where(HealthData.user_id==user_id).all()
    return health_datas        