from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import verify_password, create_access_token
from app.db.models.user import User
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Login user and generate JWT token
@router.post("/token")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}
