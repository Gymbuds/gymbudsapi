from fastapi import FastAPI
from app.db.session import check_db_connection  # Import the check_db_connection function
from app.api.endpoints import users, auth, availabilityranges, workout_logs, ai_advices, health_datas,communities
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI 
app = FastAPI(host="0.0.0.0", port=8000)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(workout_logs.router, prefix="/workout_logs", tags=["workout_logs"])
app.include_router(availabilityranges.router,prefix ="/avalrange", tags=["Availibility_range"])
app.include_router(ai_advices.router,prefix="/ai_advices", tags=["ai_advices"])
app.include_router(health_datas.router,prefix="/health_datas", tags=["health_datas"])
app.include_router(communities.router,prefix="/communities",tags=["communities"])
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
