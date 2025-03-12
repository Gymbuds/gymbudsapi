from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.workout_log import WorkoutLog, WorkoutLogCreate, WorkoutLogUpdate
from app.db.repositories.workout_log_repo import create_workout_log, update_workout_log

router = APIRouter()

# Create new log
@router.post("/log", response_model=WorkoutLog)
def create_log(workout_log: WorkoutLogCreate, db: Session = Depends(get_db)):
    return create_workout_log(db, workout_log)

# Update a workout log
@router.put("/log/{log_id}", response_model=WorkoutLog)
def update_log(log_id: int, workout_log_update: WorkoutLogUpdate, db: Session = Depends(get_db)):
    updated_log = update_workout_log(db, log_id, workout_log_update)
    
    if not updated_log:
        raise HTTPException(status_code=404, detail="Workout log not found")

    return updated_log