from app.db.database import Base
from sqlalchemy import Column,Integer,ForeignKey,String,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_url = Column(String,nullable=True)
    content = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User",back_populates="sent_messages")
