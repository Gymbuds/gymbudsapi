from app.db.database import Base
from sqlalchemy import Column,Integer,ForeignKey,Boolean,Enum
from sqlalchemy.orm import relationship
import enum
class Status(enum.Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
class MatchCandidate(Base):
    __tablename__ = "match_candidates"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False) # main person
    candidate_user_id = Column (Integer,ForeignKey('users.id'),nullable = False)
    status = Column(Enum(Status),nullable=False)
    score = Column(Integer,nullable=False)
    user = relationship("User",foreign_keys=[user_id],back_populates="candidates")
    candidate_user = relationship("User",foreign_keys=[candidate_user_id],back_populates="is_candidate_of")
     
