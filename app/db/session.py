from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from .database import engine
from sqlalchemy import text
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  
        return True
    except OperationalError as e:
        print(f"Database connection error: {e}")
        return False
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db
    finally:
        db.close()  # Close the session when done