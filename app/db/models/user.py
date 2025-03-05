from app.db.database import Base
from sqlalchemy import Column,Integer,String
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)