from app.db.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
class MatchResult(Base):
    __tablename__= "match_results"

    id = Column(Integer, primary_key=True)
    user_id1 = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_id2 = Column(Integer, ForeignKey("users.id"), nullable=False)
    matched_at = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))

    user1 = relationship("User", foreign_keys=[user_id1], back_populates="match_results1")
    user2 = relationship("User", foreign_keys=[user_id2], back_populates="match_results2")