from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_access_token, get_current_user, hash_password
from jwt import ExpiredSignatureError, InvalidTokenError
from app.db.models.user import User
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Login user and generate JWT access token
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
    
    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    # Store hashed refresh token in DB
    user.hashed_refresh_token = hash_password(refresh_token)
    db.commit()
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

#Refresh JWT token to generate new access JWT tokens
@router.post("/refresh")
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(refresh_token)  # Decode refresh token
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        # Verify the provided refresh token against the stored hashed version
        if not user.hashed_refresh_token or not verify_password(refresh_token, user.hashed_refresh_token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        new_access_token = create_access_token(data={"sub": email})  # Generate new access token

        return {"access_token": new_access_token, "token_type": "bearer"}

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

@router.post("/logout")
def logout_user(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.hashed_refresh_token = None  # Invalidate refresh token
    db.commit()
    return {"message": "Logged out successfully"}
