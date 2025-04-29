from sqlalchemy.orm import Session
from app.db.models.user_goal import UserGoal, GymGoal

def add_multiple_user_goals(db: Session, user_id: int, goals: list[GymGoal]):
    db.query(UserGoal).filter(UserGoal.user_id == user_id).delete()
    user_goals = [UserGoal(user_id=user_id, goal=goal) for goal in goals]
    db.bulk_save_objects(user_goals)
    db.commit()
    return user_goals

def get_user_goals(db: Session, user_id: int):
    """Retrieve all goals for a user."""
    return db.query(UserGoal).filter(UserGoal.user_id == user_id).all()
