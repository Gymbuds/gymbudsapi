from app.db.models.user import User
from sqlalchemy.orm import Session

def create_user(db: Session, email: str, password: str, name: str) -> User:
    db_user = User(email=email, hashed_password=password, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def update_user(db:Session, name:str, profile_picture:str, preferred_workout_goals:str, age:int, skill_level:str,user:User):
    if name:
        user.name = name
    if profile_picture:
        user.profile_picture = profile_picture
    if preferred_workout_goals:
        user.preferred_workout_goals = preferred_workout_goals
    if age:
        user.age = age
    if skill_level:
        user.skill_level = skill_level
    db.commit()
    db.refresh(user)