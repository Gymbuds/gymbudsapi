from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float,Text,DateTime
from sqlalchemy.orm import relationship
import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    hashed_refresh_token = Column(String, nullable=True)
    profile_picture = Column (String,nullable=True)
    latitude = Column(Float,nullable=True)
    longitude = Column (Float,nullable=True)
    preferred_workout_goals = Column(Text,nullable = True)
    created_at = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))

    availability_ranges = relationship("AvailabilityRange", back_populates="user", cascade="all, delete-orphan") # if one user is deleted so are all of their ranges
    workout_logs = relationship("WorkoutLog", back_populates="user", cascade="all, delete-orphan")