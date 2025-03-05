from fastapi import FastAPI, Depends,Query
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, check_db_connection  # Import the check_db_connection function
from app.db.database import Base, engine
from app.db.models.item import Item
from typing import Annotated
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
@app.get("/items/{item_id}")
async def read_item(item_id):
    return{"item_id":item_id}
@app.get("/items/")
async def read_items(q: Annotated[str | None,Query(min_length=3,max_length=50)]= None,):
    results = {"items": [{"item_id":"foo"},{"item_id":"foo"}]}
    if q:
        results.update({"q":q})
    return results
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.post("/items/")
async def create_item(item:Item):
    if item.price <= 2:
        print(item.name,item.price)
    return item
# Dependency to get the database session
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db
    finally:
        db.close()  # Close the session when done