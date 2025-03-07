from fastapi import FastAPI
from app.db.session import check_db_connection  # Import the check_db_connection function
from app.api.endpoints.init import api_router 

# Initialize FastAPI
app = FastAPI()

# Check if the database is connected at startup
@app.on_event("startup")
async def startup():
    if check_db_connection():
        print("Database connection successful!")
    else:
        print("Failed to connect to the database!")

app.include_router(api_router, prefix="/endpoints", tags=["api"])
