from fastapi import FastAPI
from app.db.session import check_db_connection  # Import the check_db_connection function

from app.api.endpoints import users, auth


from app.db.models.user import User
from app.db.session import get_db
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
# from app.db import models
load_dotenv()
# Initialize FastAPI
app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app = FastAPI(redirect_slashes=False)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    f'{os.getenv('FRONT_END_URL')}',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Check if the database is connected at startup
@app.on_event("startup")
async def startup():
    if check_db_connection():
        print("Database connection successful!")
    else:
        print("Failed to connect to the database!")


