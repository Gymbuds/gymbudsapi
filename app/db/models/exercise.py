from app.db.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Float
from sqlalchemy.orm import relationship
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_log_id = Column(Integer, ForeignKey("workout_logs.id"), nullable=False)
    exercise_name = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=True)

    workout_log = relationship("WorkoutLog", back_populates="exercises")