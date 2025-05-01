from sqlalchemy.orm import Session
from app.db.models.user_goal import UserGoal, GymGoal
from collections import defaultdict

from sqlalchemy import select,and_

def add_multiple_user_goals(db: Session, user_id: int, goals: list[GymGoal]):
    db.query(UserGoal).filter(UserGoal.user_id == user_id).delete()
    user_goals = [UserGoal(user_id=user_id, goal=goal) for goal in goals]
    db.bulk_save_objects(user_goals)
    db.commit()
    return user_goals

def get_user_goals(db: Session, user_id: int):
    """Retrieve all goals for a user."""
    return db.query(UserGoal).filter(UserGoal.user_id == user_id).all()

def get_list_user_goals_as_set(db: Session, user_id: int):
    """Retrieve all goals for a user."""
    results = db.execute(select(UserGoal.goal).where(UserGoal.user_id == user_id)).scalars().all()

    return set(results)
def get_multiple_users_goals_as_set(db:Session,user_ids: list[int]):
    dict_of_sets = defaultdict(set)

    user_goals = db.query(UserGoal).filter(
        and_(
            UserGoal.user_id.in_(user_ids),
        )
    )
    for user_goal in user_goals:
        
            dict_of_sets[user_goal.user_id].add(user_goal.goal)
    return dict_of_sets
