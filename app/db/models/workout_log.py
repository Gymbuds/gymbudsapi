from app.db.database import Base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Enum,Text
from sqlalchemy.orm import relationship
import datetime
class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(Enum("VOICE", "MANUAL", name="log_method"), nullable=False)
    notes = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    mood = Column(Enum("ENERGIZED", "TIRED", "MOTIVATED", "STRESSED", "NEUTRAL", name="mood_type"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("User", back_populates="workout_logs")
    exercises = relationship("Exercise", back_populates="workout_log", cascade="all, delete-orphan")