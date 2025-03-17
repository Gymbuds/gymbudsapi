from fastapi import APIRouter, Depends, HTTPException, status
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, get_current_user, validate_password, create_access_token, create_refresh_token
from app.db.repositories.user_repo import create_user
from sqlalchemy.orm import Session

from app.core.security import get_current_user, hash_password, validate_password
from app.db.crud.user_repo import create_user
from app.db.crud.range_crud import get_availability_ranges_user
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate

router = APIRouter()

# Register new user
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserCreate): The user data to create.
        db (Session): The database session.

    Raises:
        HTTPException: If the email is already registered or the password is invalid.

    Returns:
        dict: A success message.
    """
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

    # Create access and refresh tokens for the new user
    access_token = create_access_token(data={"sub": email_lowercase})
    refresh_token = create_refresh_token(data={"sub": email_lowercase})

    # Store the hashed refresh token in DB
    new_user.hashed_refresh_token = hash_password(refresh_token)
    db.commit()
    
    return {"success": "User created successfully", "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Get user profile
@router.get("/profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the current user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        dict: The user's profile information.
    """
    return {"name": current_user.name, "email": current_user.email}


@router.get("/availability-ranges")
def get_availability_ranges_for_user(user_email: str, db: Session = Depends(get_db)):
    """
    Get availability ranges for a user by email.

    Args:
        user_email (str): The email of the user.
        db (Session): The database session.

    Raises:
        HTTPException: If the user does not exist.

    Returns:
        User: The user object.
    """
    email_lowercase = user_email.lower()
    user = db.query(User).filter(User.email == email_lowercase).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist"
        )
    user_aval_ranges = get_availability_ranges_user(db=db,user_id=user.id)
    return user_aval_ranges
    