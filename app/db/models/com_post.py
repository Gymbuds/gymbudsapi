from app.db.database import Base
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
import datetime
class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    community_id = Column(Integer, ForeignKey("gym_communities.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("User", back_populates="community_posts")
    gym_community = relationship("Community", back_populates="community_posts")