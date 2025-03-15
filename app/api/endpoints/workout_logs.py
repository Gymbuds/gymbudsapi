from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.workout_log import WorkoutLog, WorkoutLogCreate, WorkoutLogUpdate
from app.db.models.user import User
from app.db.repositories.workout_log_repo import create_workout_log, update_workout_log, delete_workout_log, get_workout_logs_by_user
from app.core.security import get_current_user
from typing import List

router = APIRouter()

# Create new log
@router.post("/log", response_model=WorkoutLog)
def create_log(workout_log: WorkoutLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_workout_log(db, workout_log, user_id=current_user.id)

# Update a workout log
@router.put("/log/{log_id}", response_model=WorkoutLog)
def update_log(log_id: int, workout_log_update: WorkoutLogUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_log = update_workout_log(db, log_id, workout_log_update, current_user.id)
    
    if not updated_log:
        raise HTTPException(status_code=404, detail="Workout log not found")

    return updated_log

# Delete a workout log
@router.delete("/log/{log_id}", response_model=WorkoutLog)
def delete_log(log_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_log = delete_workout_log(db, log_id, current_user.id)
    
    if not deleted_log:
        raise HTTPException(status_code=404, detail="Workout log not found")
    
    return deleted_log

# Get all workout logs
@router.get("", response_model=List[WorkoutLog])
def get_logs(current_user: User = Depends(get_current_user), db:Session = Depends(get_db)):
    user_id = current_user.id
    log = get_workout_logs_by_user(db=db, user_id=user_id)
    return log