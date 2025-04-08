from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float


class Community(Base):
    __tablename__ = "gym_communities"
    id = Column(Integer,primary_key=True)
    address = Column(String,primary_key=True)
    latitude = Column(Float,nullable=True)
    longitude = Column (Float,nullable=True)
    profile_picture = Column (String,nullable=True)
    member_count = Column (Integer,default=0)