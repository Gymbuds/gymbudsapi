from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime
import datetime
class WorkoutLog(Base):
    __tablename__ = "workout_log"

    id = Column(Integer, primary_key=True, index=True)
    exercise = Column(String, index=True)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float, nullable=True)
    mood = Column(String, nullable=True)
    created_at = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))