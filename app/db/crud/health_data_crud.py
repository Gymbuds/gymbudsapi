from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.models.health_data import HealthData
from app.schemas.health_data import HealthDataCreate

#Create a new health data entry
def create_health_data(db: Session, user_id: int, health_data: HealthDataCreate) -> HealthData:
    db_health = HealthData(
        user_id=user_id, 
        steps=health_data.steps,
        calories_burnt=health_data.calories_burnt,
        avg_heart_rate=health_data.avg_heart_rate,
        sleep_duration=health_data.sleep_duration,
        active_mins=health_data.active_mins
    )
    db.add(db_health)
    db.commit()
    db.refresh(db_health)
    return db_health
