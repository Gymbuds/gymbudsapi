from fastapi import FastAPI
from app.db.session import check_db_connection  # Import the check_db_connection function

from app.api.endpoints import users, auth, workout_logs
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI 
app = FastAPI(host="0.0.0.0", port=8000)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(workout_logs.router, prefix="/workout_logs", tags=["workout_logs"])

# CORS Middleware Configuration
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    os.getenv("FRONT_END_URL"),
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
