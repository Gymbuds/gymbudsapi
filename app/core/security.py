from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError, encode, decode
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.models.user import User
from app.core.config import settings
from app.db.session import get_db
from sqlalchemy.orm import Session
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize HTTPBearer security
security = HTTPBearer()

# Hashes a password using bcrypt
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verifies if a plain password matches a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generates a JWT access token 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # Access token expires in 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Decode JWT token
def decode_access_token(token: str):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
#Get current user
def get_current_user(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials  # Get the token from HTTPAuthorizationCredentials
    payload = decode_access_token(token)
    
    # Use the 'sub' claim (email) to find the user
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user is None:
        raise credentials_exception
    return user

#Make sure password is valid
def validate_password(password: str) -> bool:
    # Minimum length of 8 characters, at least one digit, one uppercase letter, one lowercase letter, and one special character.
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):  # At least one cap letter
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):  # At least one lower letter
        return "Password must contain at least one lowecase letter."
    if not re.search(r'[0-9]', password):  # At least one digit
        return "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # At least one special character
        return "Password must contain at least one special character."
    return "Password is valid."