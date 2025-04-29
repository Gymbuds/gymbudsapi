from app.db.models.user import User
from sqlalchemy.orm import Session

def create_user(db: Session, email: str, password: str, name: str) -> User:
    db_user = User(email=email, hashed_password=password, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def update_user(db:Session, name:str, profile_picture:str, age:int, skill_level:str,weight:int,gender:str,zip_code:int,user:User):
    if name:
        user.name = name
    if profile_picture:
        user.profile_picture = profile_picture
    if age:
        user.age = age
    if skill_level:
        user.skill_level = skill_level
    if weight:
        user.weight = weight
    if gender:
        user.gender = gender
    if zip_code:
        user.zip_code = zip_code
    db.commit()
    db.refresh(user)  
def get_user_info_by_id(db:Session,user_id:int):
    user = db.query(User).filter(User.id==user_id).first()
    return user


def get_multiple_users_info_by_ids(db: Session, user_ids: list[int]):
    if not user_ids:
        return []

    users = db.query(User).filter(User.id.in_(user_ids)).all()
    return users
  