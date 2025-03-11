from app.db.models.workout_log import WorkoutLog
from sqlalchemy.orm import Session
from app.schemas.workout_log import WorkoutLogCreate

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
