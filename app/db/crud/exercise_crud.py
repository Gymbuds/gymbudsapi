from app.db.models.exercise import Exercise
from sqlalchemy.orm import Session
from app.schemas.workout_log import ExerciseDetailResponse
from typing import List, Optional

# Add new exercises
def add_exercise(db: Session, workout_log_id: int, exercise_name: str, sets: int, reps: int, weight: Optional[float] = None):
    new_exercise = Exercise(
        workout_log_id=workout_log_id,
        exercise_name=exercise_name,
        sets=sets,
        reps=reps,
        weight=weight
    )
    db.add(new_exercise)
    db.commit()  # Ensure it's saved in the database
    db.refresh(new_exercise)  # Get the ID
    return new_exercise  # Return the full exercise object

# Update existing exercises
def update_exercise(db: Session, exercise_id: int, exercise_name: Optional[str] = None, sets: Optional[int] = None, reps: Optional[int] = None, weight: Optional[float] = None) -> Optional[Exercise]:
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if db_exercise:
        if exercise_name is not None:
            db_exercise.exercise_name = exercise_name
        if sets is not None:
            db_exercise.sets = sets
        if reps is not None:
            db_exercise.reps = reps
        if weight is not None:
            db_exercise.weight = weight
        db.commit()
        db.refresh(db_exercise)
        return db_exercise
    return None

# Delete an exercise
def delete_exercise(db: Session, exercise_id: int) -> Optional[Exercise]:
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if db_exercise:
        db.delete(db_exercise)
        db.commit()
        return db_exercise
    return None

# Delete all exercises linked to a workout log
def delete_exercises_by_workout_log(db: Session, workout_log_id: int):
    db.query(Exercise).filter(Exercise.workout_log_id == workout_log_id).delete()
    db.commit()

# Fetch exercises for a workout log
def get_exercises_by_workout(db: Session, workout_log_id: int) -> List[ExerciseDetailResponse]:
    exercises = db.query(Exercise).filter(Exercise.workout_log_id == workout_log_id).all()
    return [ExerciseDetailResponse(
        exercise_id=e.id,
        exercise_name=e.exercise_name,
        sets=e.sets,
        reps=e.reps,
        weight=e.weight
    ) for e in exercises]
