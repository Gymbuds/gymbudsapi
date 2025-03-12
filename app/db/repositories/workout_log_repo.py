from app.db.models.workout_log import WorkoutLog
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogUpdate

def create_workout_log(db: Session, workout_log: WorkoutLogCreate) -> WorkoutLog:
    db_workout = WorkoutLog(
        user_id=workout_log.user_id,
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

def update_workout_log(db: Session, log_id: int, workout_log_update: WorkoutLogUpdate) -> WorkoutLog:
    db_workout = db.query(WorkoutLog).filter(WorkoutLog.id == log_id).first()

    if not db_workout:
        return None  # Handle in the route

    # Update fields if provided, otherwise retain existing values
    if workout_log_update.title is not None:
        db_workout.title = workout_log_update.title
    if workout_log_update.type is not None:
        db_workout.type = workout_log_update.type.value

    if workout_log_update.exercise_details is not None:
        existing_exercises = db_workout.exercise_details
        new_exercises = workout_log_update.exercise_details

        # Create a dictionary of existing exercises by exercise name
        existing_exercise_dict = {e['exercise']: e for e in existing_exercises}

        # Iterate through the new exercises
        for new_exercise in new_exercises:
            if new_exercise.exercise in existing_exercise_dict:
                # If exercise exists, update it
                existing_exercise_dict[new_exercise.exercise].update({
                    'weight': new_exercise.weight,
                    'sets': new_exercise.sets,
                    'reps': new_exercise.reps
                })
            else:
                # If exercise doesn't exist, add it to the dictionary
                existing_exercise_dict[new_exercise.exercise] = new_exercise.dict()

        # Convert the updated dictionary back to a list
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

# Fetch all workout logs for a given user by ID
def get_workout_logs_by_user(db: Session, user_id: int):
    result = db.execute(select(WorkoutLog).where(WorkoutLog.user_id == user_id))
    return result.scalars().all()