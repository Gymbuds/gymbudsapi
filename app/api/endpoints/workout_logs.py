from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.workout_log import WorkoutLog, WorkoutLogCreate
from app.db.repositories.workout_log_repo import create_workout_log

router = APIRouter()

@router.post("/log", response_model=WorkoutLog)
def create_log(workout_log: WorkoutLogCreate, db: Session = Depends(get_db)):
    return create_workout_log(db, workout_log)