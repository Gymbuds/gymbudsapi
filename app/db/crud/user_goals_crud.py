# app/db/crud/user_goals_crud.py

from sqlalchemy.orm import Session
from app.db.models.user_goal import UserGoal, GymGoal

def add_user_goal(db: Session, user_id: int, goal: GymGoal):
    user_goal = UserGoal(user_id=user_id, goal=goal)
    db.add(user_goal)
    db.commit()
    db.refresh(user_goal)
    return user_goal

def add_multiple_user_goals(db: Session, user_id: int, goals: list[GymGoal]):
    user_goals = [UserGoal(user_id=user_id, goal=goal) for goal in goals]
    db.bulk_save_objects(user_goals)
    db.commit()
    return user_goals

def get_user_goals(db: Session, user_id: int):
    """Retrieve all goals for a user."""
    return db.query(UserGoal).filter(UserGoal.user_id == user_id).all()

def delete_user_goal(db: Session, user_id: int, goal: GymGoal):
    """Delete a specific goal for a user."""
    user_goal = db.query(UserGoal).filter(UserGoal.user_id == user_id, UserGoal.goal == goal).first()
    if user_goal:
        db.delete(user_goal)
        db.commit()
    return user_goal

def delete_all_user_goals(db: Session, user_id: int):
    """Delete all goals for a user."""
    db.query(UserGoal).filter(UserGoal.user_id == user_id).delete()
    db.commit()
