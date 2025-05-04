from fastapi import APIRouter, Depends, HTTPException, status
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.db.crud.user_crud import create_user,update_user
from sqlalchemy.orm import Session
from app.core.security import get_current_user, hash_password, validate_password
from app.core.security import hash_password, get_current_user, validate_password, create_access_token, create_refresh_token
from app.core.s3 import create_presigned_upload_url
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import UserCreate,UserUpdate
from app.db.crud.community_crud import get_user_preferred_gym,get_user_gyms,get_community_by_id
from app.db.crud.match_preferences_crud import create_match_preference

router = APIRouter()

# Register new user
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user and generate an access token.

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

    create_match_preference(db, new_user.id)
    
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
    return {"user": current_user}

@router.patch("/profile/update")
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update user profile information.
    """
    if not any([user_update.name, user_update.profile_picture, user_update.age, user_update.skill_level, user_update.weight, user_update.gender, user_update.zip_code, user_update.latitude, user_update.longitude]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update."
        )

    update_user(
        db=db,
        name=user_update.name,
        profile_picture=user_update.profile_picture,
        age=user_update.age,
        skill_level=user_update.skill_level,
        weight=user_update.weight,
        gender=user_update.gender,
        zip_code=user_update.zip_code,
        longitude=user_update.longitude,
        latitude=user_update.latitude,
        user=current_user
    )

    return {"success": "User profile updated successfully", "user": current_user}

@router.get("/profile/generate-upload-url/")
def generate_upload_url(
    file_extension: str,  # example: "jpeg", "png"
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file_extension not in ["jpeg", "jpg", "png"]:
        raise HTTPException(status_code=400, detail="Invalid file extension")

    presigned_url, s3_file_url = create_presigned_upload_url(
        user_id=current_user.id,
        file_extension=file_extension,
        folder="profile_pictures"
    )
    return {
        "upload_url": presigned_url,  # Used by frontend to PUT the image
        "file_url": s3_file_url       # Final S3 URL to save into DB
    }

@router.get("/prefer")
def get_preferred_community(db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return get_user_preferred_gym(db,current_user.id)

@router.get("/gyms")
def get_current_user_gyms(db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    list_user_communities = get_user_gyms(db=db,user_id=current_user.id)
    community_list = []
    for user_community in list_user_communities:
        community = get_community_by_id(db=db,community_id=user_community.community_id)
        community_list.append(community)
    return community_list


