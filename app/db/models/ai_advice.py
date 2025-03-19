from app.db.database import Base
from sqlalchemy import Column,Integer,String,Enum,DateTime,ForeignKey
from sqlalchemy.orm import relationship
import datetime
from app.schemas.advice import AIAdviceType
class AIAdvice(Base):
    __tablename__="ai_advices"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    advice_type=Column(Enum(AIAdviceType),nullable=False)
    ai_feedback=Column(String,nullable=True)
    created_at=Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))
    
    user = relationship("User",back_populates="ai_advices")