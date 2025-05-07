from app.db.database import Base
from sqlalchemy import Integer,Column,DateTime,ForeignKey
from sqlalchemy.orm import relationship
import datetime
class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))

    user1 = relationship("User", foreign_keys=[user1_id],back_populates="user_chats_1")
    user2 = relationship("User", foreign_keys=[user2_id],back_populates="user_chats_2")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
