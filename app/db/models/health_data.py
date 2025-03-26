from app.db.database import Base
from sqlalchemy import Column,Integer,Float,Date,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
class HealthData(Base):
    __tablename__ = "health_datas"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=datetime.now(timezone.utc).date())
    steps = Column(Integer, nullable=False, default=0)
    calories_burnt = Column(Float, nullable=False, default=0)
    avg_heart_rate = Column(Integer, nullable=True)
    sleep_duration = Column(Float, nullable=True)
    active_mins = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="health_datas")