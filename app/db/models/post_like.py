from app.db.database import Base
from sqlalchemy import Column,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
                        
    user = relationship("User", back_populates="post_likes")
    community_post = relationship("CommunityPost", back_populates="post_likes")
