from app.db.database import Base
from sqlalchemy import Column,Integer,ForeignKey,Enum
from sqlalchemy.orm import relationship

class MatchPreference(Base):
    __tablename__ = "match_preferences"

    id= Column(Integer,primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    gender = Column(Enum("MALE", "FEMALE", "BOTH", name="gender"), nullable=False)
    start_weight = Column(Integer,nullable =False)
    end_weight = Column(Integer,nullable =False)
    max_location_distance_miles = Column(Integer,nullable=False)

    user = relationship("User", back_populates="match_preferences")