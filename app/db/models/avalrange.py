from sqlalchemy import Column,Integer,Time,Enum,ForeignKey
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base
class DayOfWeek(enum.Enum):
    Monday = "MONDAY"
    Tuesday = "TUESDAY"
    Wednesday = "WEDNESDAY"
    Thursday = "THURSDAY"
    Friday = "FRIDAY"
    Saturday = "SATURDAY"
    Sunday = "SUNDAY"
class AvailabilityRange(Base):
    __tablename__ = "availability_ranges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column (Integer,ForeignKey('users.id'),nullable=False)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False) 
    end_time = Column(Time, nullable=False)
    
    user = relationship("User",back_populates="availability_ranges")