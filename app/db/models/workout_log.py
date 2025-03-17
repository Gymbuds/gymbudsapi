from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Enum,JSON,Text
from sqlalchemy.orm import relationship
import datetime
class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(Enum("Voice", "Manual", name="log_method"), nullable=False)
    exercise_details = Column(JSON, nullable=False)  # Example: [{"exercise": "Squat", "sets": 3, "reps": 10, "weight": null}]
    notes = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    mood = Column(Enum("Energized", "Tired", "Motivated", "Stressed", "Neutral", name="mood_type"), nullable=False)
    date = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))
    
    user = relationship("User", back_populates="workout_logs")