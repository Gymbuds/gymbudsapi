from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.db.session import check_db_connection  # Import the check_db_connection function
# from app.db.models.user import User
# from app.core.security import hash_password, create_access_token, decode_access_token
# from app.db.session import get_db
# from pydantic import BaseModel, EmailStr
from app.api.endpoints.init import api_router 
# from app.db import models

# Initialize FastAPI
app = FastAPI()

# Check if the database is connected at startup
@app.on_event("startup")
async def startup():
    if check_db_connection():
        print("Database connection successful!")
    else:
        print("Failed to connect to the database!")

# class UserCreate(BaseModel):
#     name: str
#     email: EmailStr
#     password: str

# @app.post("/users/")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     hashed_password = hash_password(user.password)
#     db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)

#     # Check if email exists
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Generate JWT token
#     token = create_access_token({"sub": user.email})

#     db_user.JWT_token = token  # Store token in DB

#     # Decode the token and store decoded information
#     decoded_info = decode_access_token(token)
#     db_user.decoded_token_info = decoded_info # Store decode info in DB

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

app.include_router(api_router, prefix="/endpoints", tags=["api"])

# Dependency to get the database session
