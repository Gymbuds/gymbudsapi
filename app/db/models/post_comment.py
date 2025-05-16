from app.db.database import Base
from sqlalchemy import Column,Integer,Text,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="post_comments")
    community_post = relationship("CommunityPost", back_populates="post_comments")