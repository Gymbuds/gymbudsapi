from app.db.models.user import User
from sqlalchemy.orm import Session

def create_user(db: Session, email: str, password: str, name: str) -> User:
    db_user = User(email=email, hashed_password=password, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
