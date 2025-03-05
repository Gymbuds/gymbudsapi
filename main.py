from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.session import check_db_connection  # Import the check_db_connection function
from app.db.models.user import User
from app.db.session import get_db
from pydantic import BaseModel
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

class UserCreate(BaseModel):
    name: str

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Dependency to get the database session
