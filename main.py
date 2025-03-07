from fastapi import FastAPI
from app.db.session import check_db_connection  # Import the check_db_connection function

from app.api.endpoints import users, auth


# Initialize FastAPI
app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
# Check if the database is connected at startup
@app.on_event("startup")
async def startup():
    if check_db_connection():
        print("Database connection successful!")
    else:
        print("Failed to connect to the database!")


