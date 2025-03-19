from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_access_token, get_current_user, hash_password, create_password_reset_token, validate_password
from jwt import ExpiredSignatureError, InvalidTokenError
from app.db.models.user import User
from app.schemas.user import Login, RefreshToken, PasswordResetRequest, ResetPassword
from app.db.session import get_db
from app.services.email_service import send_reset_email
from sqlalchemy.orm import Session
from pydantic import BaseModel

import secrets, string
reset_tokens = {}  # Simple in-memory store for mapping a short code to the full reset token

router = APIRouter()

# Login user and generate JWT access token
@router.post("/login")
def login_user(request: Login, db: Session = Depends(get_db)):
    # Convert the input email to lowercase
    email_lowercase = request.email.lower()

    # Find user by email
    user = db.query(User).filter(User.email == email_lowercase).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": email_lowercase})
    refresh_token = create_refresh_token(data={"sub": email_lowercase})

    # Store hashed refresh token in DB
    user.hashed_refresh_token = hash_password(refresh_token)
    db.commit()
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Refresh JWT token to generate new access JWT tokens
@router.post("/refresh")
def refresh_access_token(request: RefreshToken, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(request.refresh_token)  # Decode refresh token
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        # Verify the provided refresh token against the stored hashed version
        if not user.hashed_refresh_token or not verify_password(request.refresh_token, user.hashed_refresh_token):
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

# Request password reset
@router.post("/request-password-reset")
async def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    email_lowercase = request.email.lower()
    user = db.query(User).filter(User.email == email_lowercase).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Create the full JWT reset token (expires in 15 minutes)
    reset_token = create_password_reset_token(data={"sub": email_lowercase})
    
    # Generate a short reset code (6-character alphanumeric)
    short_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    
    reset_tokens[short_code] = reset_token
    
    # Send reset code via email
    await send_reset_email(email=email_lowercase, code=short_code)
    
    return {"success": "Password reset email sent", "reset_code": short_code}

class VerifyResetCode(BaseModel):
    code: str

@router.post("/verify-reset-code")
def verify_reset_code(request: VerifyResetCode):
    token = reset_tokens.get(request.code)
    if not token:
        raise HTTPException(status_code=404, detail="Invalid or expired reset code")
    # Remove the code once used (to prevent reuse)
    reset_tokens.pop(request.code, None)
    return {"token": token}

# Reset password after verifying token
@router.post("/reset-password")
def reset_password(request: ResetPassword, db: Session = Depends(get_db)):
    try:
        # Decode the token
        payload = decode_access_token(request.reset_token)

        # Get the user from the payload
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Convert the email to lowercase for the lookup
        email_lowercase = email.lower()

        # Retrieve the user from the database
        user = db.query(User).filter(User.email == email_lowercase).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Validate the password
        validation_result = validate_password(request.new_password)
        if validation_result != "Password is valid.":
            raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
                detail=validation_result
            )
    
        # Update the user's password in the database
        user.hashed_password = hash_password(request.new_password)
        db.commit()

        return {"success": "Password successfully reset."}
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Reset token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid reset token")