from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship

class Community(Base):
    __tablename__ = "gym_communities"
    id = Column(Integer,primary_key=True)
    address = Column(String,primary_key=True)
    latitude = Column(Float,nullable=True)
    longitude = Column (Float,nullable=True)
    profile_picture = Column (String,nullable=True)
    member_count = Column (Integer,default=0)

    community_posts = relationship("CommunityPost", back_populates="gym_community", cascade="all, delete-orphan")