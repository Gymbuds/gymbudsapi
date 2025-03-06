from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError, encode, decode
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.db.models.user import User
from app.core.config import settings
from app.db.session import get_db
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Hashes a password using bcrypt
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#Verifies if a plain password matches a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Generates a JWT access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

#Decode JWT token
def decode_access_token(token: str):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Decode the token and handle potential errors
    payload = decode_access_token(token)
    
    # Use the 'sub' claim (typically the username or email) to find the user
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user is None:
        raise credentials_exception
    return user