from fastapi import APIRouter, Depends, HTTPException, status
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, get_current_user
from app.db.repositories.user_repo import create_user
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

# Register new user
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create the user in the database
    new_user = create_user(db=db, email=user.email, password=hashed_password, name=user.name)
    
    return {"message": "User created successfully"}

