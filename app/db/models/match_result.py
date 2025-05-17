from app.db.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
class MatchResult(Base):
    __tablename__= "match_results"

    id = Column(Integer, primary_key=True)
    user_id1 = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_id2 = Column(Integer, ForeignKey("users.id"), nullable=False)
    matched_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user1 = relationship("User", foreign_keys=[user_id1], back_populates="match_results1")
    user2 = relationship("User", foreign_keys=[user_id2], back_populates="match_results2")