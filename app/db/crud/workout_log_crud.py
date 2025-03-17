from app.db.models.workout_log import WorkoutLog
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogUpdate
from typing import Optional

def create_workout_log(db: Session, workout_log: WorkoutLogCreate, user_id = int) -> WorkoutLog:
    db_workout = WorkoutLog(
        user_id=user_id,
        title=workout_log.title,
        type=workout_log.type.value,
        exercise_details=[exercise.dict() for exercise in workout_log.exercise_details],
        notes=workout_log.notes,
        duration_minutes=workout_log.duration_minutes,
        mood=workout_log.mood.value
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

def update_workout_log(db: Session, log_id: int, workout_log_update: WorkoutLogUpdate, user_id: int) -> Optional[WorkoutLog]:
    db_workout = db.query(WorkoutLog).filter(WorkoutLog.id == log_id, WorkoutLog.user_id == user_id).first()

    if not db_workout:
        return None

    # Update fields if provided
    if workout_log_update.title is not None:
        db_workout.title = workout_log_update.title
    if workout_log_update.type is not None:
        db_workout.type = workout_log_update.type.value

    if workout_log_update.exercise_details is not None or workout_log_update.delete_exercises is not None:
        existing_exercises = db_workout.exercise_details  # List of existing exercises
        new_exercises = workout_log_update.exercise_details or []  # Avoid None issues

        # Convert existing exercises into a dictionary for easy lookup
        existing_exercise_dict = {e['exercise']: e for e in existing_exercises}

        # Update or add exercises from new_exercises
        for new_exercise in new_exercises:
            existing_exercise_dict[new_exercise.exercise] = new_exercise.dict()

        # Delete exercises if they are listed in `delete_exercises`
        if workout_log_update.delete_exercises:
            for exercise in workout_log_update.delete_exercises:
                existing_exercise_dict.pop(exercise, None)  # Remove safely if it exists

        # Convert dictionary back to a list
        db_workout.exercise_details = list(existing_exercise_dict.values())

    if workout_log_update.notes is not None:
        db_workout.notes = workout_log_update.notes
    if workout_log_update.duration_minutes is not None:
        db_workout.duration_minutes = workout_log_update.duration_minutes
    if workout_log_update.mood is not None:
        db_workout.mood = workout_log_update.mood.value

    db.commit()
    db.refresh(db_workout)
    return db_workout

def delete_workout_log(db: Session, log_id:int, user_id:int):
    db_workout = db.query(WorkoutLog).filter(WorkoutLog.id == log_id, WorkoutLog.user_id == user_id).first()

    if not db_workout:
        return None  # Handle this in the route, returning 404 if not found
    
    db.delete(db_workout)
    db.commit()  # Commit the transaction to delete the record
    return db_workout

# Fetch all workout logs for a given user by ID
def get_workout_logs_by_user(db: Session, user_id: int):
    result = db.execute(select(WorkoutLog).where(WorkoutLog.user_id == user_id))
    return result.scalars().all()