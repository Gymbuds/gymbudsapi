from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship

class Community(Base):
    __tablename__ = "gym_communities"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    address = Column(String,nullable=False)
    latitude = Column(Float,nullable=True)
    longitude = Column (Float,nullable=True)


    community_posts = relationship("CommunityPost", back_populates="gym_community", cascade="all, delete-orphan")
