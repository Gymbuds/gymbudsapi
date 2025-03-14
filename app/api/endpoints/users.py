from fastapi import APIRouter, Depends, HTTPException, status
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.schemas.workout_log import WorkoutLog
from app.core.security import hash_password, get_current_user, validate_password
from app.db.repositories.workout_log_repo import get_workout_logs_by_user
from app.db.repositories.user_repo import create_user
from sqlalchemy.orm import Session
from app.db.session import get_db
from typing import List

router = APIRouter()

# Register new user
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Convert the input email to lowercase
    email_lowercase = user.email.lower()

    # Check if the user already exists by the lowercase email
    existing_user = db.query(User).filter(User.email == email_lowercase).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate the password
    validation_result = validate_password(user.password)
    if validation_result != "Password is valid.":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation_result
        )
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create the user in the database with the lowercase email
    new_user = create_user(db=db, email=email_lowercase, password=hashed_password, name=user.name)
    
    return {"success": "User created successfully"}


# Get user profile
@router.get("/profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    return {"name": current_user.name, "email": current_user.email}
