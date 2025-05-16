from app.db.database import Base
from sqlalchemy import Integer,Column,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    user_id1 = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_id2 = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user1 = relationship("User", foreign_keys=[user_id1],back_populates="user_chats_1")
    user2 = relationship("User", foreign_keys=[user_id2],back_populates="user_chats_2")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
