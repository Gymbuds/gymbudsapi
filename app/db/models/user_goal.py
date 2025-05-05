from app.db.database import Base
from sqlalchemy import Column,Integer,ForeignKey,Boolean,Enum
from sqlalchemy.orm import relationship
import enum


class GymGoal(enum.Enum):
    BUILD_MUSCLE = "BUILD_MUSCLE"
    LOSE_WEIGHT = "LOSE_WEIGHT"
    GAIN_STRENGTH = "GAIN_STRENGTH"
    IMPROVE_ENDURANCE = "IMPROVE_ENDURANCE"
    IMPROVE_OVERALL_HEALTH = "IMPROVE_OVERALL_HEALTH"
    IMPROVE_ATHLETIC_PERFORMANCE = "IMPROVE_ATHLETIC_PERFORMANCE"

class UserGoal(Base):
    __tablename__ = "user_goals"
    id = Column(Integer,primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal = Column(Enum(GymGoal), nullable=False)
    user = relationship("User", back_populates="goals")

