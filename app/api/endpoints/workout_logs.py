from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.workout_log import WorkoutLog, WorkoutLogCreate, WorkoutLogUpdate
from app.db.models.user import User
from app.db.crud.workout_log_crud import create_workout_log, update_workout_log, delete_workout_log, get_workout_logs_by_user
from app.core.security import get_current_user
from typing import List

router = APIRouter()

# Create new log
@router.post("/log", response_model=WorkoutLog)
def create_log(workout_log: WorkoutLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new workout log for the authenticated user.
    
    Args:
        workout_log (WorkoutLogCreate): The workout log data to be created.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Raises:
        HTTPException: If the user is not authenticated or there is a database error.

    Returns:
        WorkoutLog: The created workout log.
    """
    return create_workout_log(db, workout_log, user_id=current_user.id)

# Update a workout log
@router.put("/log/{log_id}", response_model=WorkoutLog)
def update_log(log_id: int, workout_log_update: WorkoutLogUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update an existing workout log for the authenticated user.

    Args:
        log_id (int): The ID of the workout log to be updated.
        workout_log_update (WorkoutLogUpdate): The updated workout log data.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Raises:
        HTTPException: If the workout log is not found, or the user is not authorized to update it.

    Returns:
        WorkoutLog: The updated workout log.
    """
    updated_log = update_workout_log(db, log_id, workout_log_update, current_user.id)
    
    if not updated_log:
        raise HTTPException(status_code=404, detail="Workout log not found")

    return updated_log

# Delete a workout log
@router.delete("/log/{log_id}", response_model=WorkoutLog)
def delete_log(log_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete a workout log for the authenticated user.

    Args:
        log_id (int): The ID of the workout log to be deleted.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Raises:
        HTTPException: If the workout log is not found or the user is not authorized to delete it.

    Returns:
        WorkoutLog: The deleted workout log.
    """
    deleted_log = delete_workout_log(db, log_id, current_user.id)
    
    if not deleted_log:
        raise HTTPException(status_code=404, detail="Workout log not found")
    
    return deleted_log

# Get all workout logs
@router.get("", response_model=List[WorkoutLog])
def get_logs(current_user: User = Depends(get_current_user), db:Session = Depends(get_db)):
    """
    Retrieve all workout logs for the authenticated user.

    Args:
        current_user (User): The currently authenticated user.
        db (Session): The database session.

    Raises:
        HTTPException: If the user is not authenticated or there is a database error.

    Returns:
        List[WorkoutLog]: A list of the authenticated user's workout logs.
    """
    log = get_workout_logs_by_user(db=db, user_id=current_user.id)
    return log