from app.db.models.workout_log import WorkoutLog
from app.db.models.exercise import Exercise
from sqlalchemy.orm import Session
from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogUpdate
from typing import Optional
from datetime import datetime, timedelta
from app.db.crud.exercise_crud import add_exercise, update_exercise, delete_exercise, delete_exercises_by_workout_log, get_exercises_by_workout


# Create a workout log for an authenticated user
def create_workout_log(db: Session, workout_log_create: WorkoutLogCreate, user_id: int) -> WorkoutLog:
    # Create the workout log entry in the database
    db_workout = WorkoutLog(
        user_id=user_id,
        title=workout_log_create.title,
        type=workout_log_create.type.value,
        notes=workout_log_create.notes,
        duration_minutes=workout_log_create.duration_minutes,
        mood=workout_log_create.mood.value,
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)  # Refresh to get ID

    # Add exercises
    for exercise in workout_log_create.exercise_details:
        add_exercise(
            db, db_workout.id, exercise.exercise_name, exercise.sets, exercise.reps, exercise.weight
        )

    # Attach exercises to the workout log in the response
    db_workout.exercise_details = get_exercises_by_workout(db, db_workout.id)

    return db_workout

# Update a workout log for an authenticated user
def update_workout_log(db: Session, log_id: int, workout_log_update: WorkoutLogUpdate, user_id: int) -> Optional[WorkoutLog]:
    db_workout = db.query(WorkoutLog).filter(WorkoutLog.id == log_id, WorkoutLog.user_id == user_id).first()

    if not db_workout:
        return None

    # Update workout log details
    if workout_log_update.title is not None:
        db_workout.title = workout_log_update.title
    if workout_log_update.type is not None:
        db_workout.type = workout_log_update.type.value
    if workout_log_update.notes is not None:
        db_workout.notes = workout_log_update.notes
    if workout_log_update.duration_minutes is not None:
        db_workout.duration_minutes = workout_log_update.duration_minutes
    if workout_log_update.mood is not None:
        db_workout.mood = workout_log_update.mood.value

    # Handle exercise updates
    if workout_log_update.exercise_details is not None:
        for exercise in workout_log_update.exercise_details:
            if exercise.exercise_id:  # If exercise ID is provided, update the existing exercise
                db_exercise = db.query(Exercise).filter(Exercise.id == exercise.exercise_id, Exercise.workout_log_id == log_id).first()
                if db_exercise:
                    update_exercise(db, exercise.exercise_id, exercise.exercise_name, exercise.sets, exercise.reps, exercise.weight)
            else:  # Otherwise, add a new exercise
                add_exercise(db, db_workout.id, exercise.exercise_name, exercise.sets, exercise.reps, exercise.weight)

    # Delete specified exercises
    if workout_log_update.delete_exercises:
        for exercise_id in workout_log_update.delete_exercises:
            delete_exercise(db, exercise_id)

    db.commit()
    db.refresh(db_workout)

    # Attach exercises to the workout log in the response
    db_workout.exercise_details = get_exercises_by_workout(db, db_workout.id)
    return db_workout

# Delete a workout log for an authenticated user
def delete_workout_log(db: Session, log_id: int, user_id: int):
    db_workout = db.query(WorkoutLog).filter(WorkoutLog.id == log_id, WorkoutLog.user_id == user_id).first()

    if not db_workout:
        return None

    # Delete all exercises related to the workout log
    delete_exercises_by_workout_log(db, log_id)

    # Delete the workout log itself
    db.delete(db_workout)
    db.commit()

    # Ensure exercise_details is included in response
    db_workout.exercise_details = []    

    return db_workout

# Fetch all workout logs for an authenticated user
def get_workout_logs_by_user(db: Session, user_id: int):
    workout_logs = db.query(WorkoutLog).filter(WorkoutLog.user_id == user_id).all()

    # Attach exercises to the workout log in the response
    for workout_log in workout_logs:
        workout_log.exercise_details = get_exercises_by_workout(db, workout_log.id)

    return workout_logs
def get_workout_logs_by_user_latest(db:Session,user_id:int,latest_amt_days:int):
    date_threshold = datetime.now() - timedelta(days=latest_amt_days) # calculate how far back we need to go for users workouts

    workout_query = db.query(WorkoutLog).filter(WorkoutLog.user_id==user_id,WorkoutLog.date > date_threshold)
    workout_logs = workout_query.all()
    if not workout_logs:
        return None,None,None
    earliest_date = workout_query.order_by(WorkoutLog.date).first().date if workout_query.count() > 0 else None
    latest_date = workout_query.order_by(WorkoutLog.date.desc()).first().date if workout_query.count() > 0 else None
    for workout_log in workout_logs:
        workout_log.exercise_details = get_exercises_by_workout(db, workout_log.id)
    return workout_logs,earliest_date,latest_date