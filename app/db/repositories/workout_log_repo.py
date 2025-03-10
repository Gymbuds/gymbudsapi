from app.db.models.workout_log import WorkoutLog
from sqlalchemy.orm import Session
from app.schemas.workout_log import WorkoutLogCreate

def create_workout_log(db: Session, workout_log: WorkoutLogCreate) -> WorkoutLog:
    db_workout = WorkoutLog(
        exercise=workout_log.exercise,
        sets=workout_log.sets,
        reps=workout_log.reps,
        weight=workout_log.weight,
        mood=workout_log.mood
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout
