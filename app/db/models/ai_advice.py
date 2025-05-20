from app.db.database import Base
from sqlalchemy import Column,Integer,String,Enum,DateTime,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from app.schemas.advice import AIAdviceType
class AIAdvice(Base):
    __tablename__="ai_advices"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    advice_type=Column(Enum(AIAdviceType),nullable=False)
    ai_feedback=Column(String,nullable=True)
    created_at=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    workout_earliest_date = Column(DateTime,nullable=True)
    workout_latest_date= Column(DateTime,nullable=True)
    contains_health_data = Column(Boolean)
    user = relationship("User",back_populates="ai_advices")