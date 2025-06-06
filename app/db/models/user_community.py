from app.db.database import Base
from sqlalchemy import Column,Integer,ForeignKey,Boolean
from sqlalchemy.orm import relationship

class UserCommunity(Base):
    __tablename__ = "user_communities"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    community_id = Column(Integer, ForeignKey("gym_communities.id", ondelete="CASCADE"), primary_key=True)
    is_preferred_gym = Column(Boolean,nullable=False)
    user = relationship("User", back_populates="user_communities_link")
    community = relationship("Community", back_populates="user_communities_link")
