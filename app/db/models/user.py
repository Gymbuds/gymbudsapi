from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float,Text,DateTime,Enum
from sqlalchemy.orm import relationship
import datetime
import enum
class SkillLevel(enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    hashed_refresh_token = Column(String, nullable=True)
    profile_picture = Column (String,nullable=True)
    latitude = Column(Float,nullable=True)
    longitude = Column (Float,nullable=True)
    preferred_workout_goals = Column(Text,nullable = True)
    created_at = Column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))
    age = Column(Integer,nullable=True)
    skill_level = Column(Enum(SkillLevel), nullable=True)
    weight = Column(Integer,nullable=True)

    
    availability_ranges = relationship("AvailabilityRange", back_populates="user", cascade="all, delete-orphan") # if one user is deleted so are all of their ranges
    workout_logs = relationship("WorkoutLog", back_populates="user", cascade="all, delete-orphan")
    ai_advices = relationship("AIAdvice", back_populates="user", cascade="all, delete-orphan")
    health_datas = relationship("HealthData", back_populates="user", cascade="all, delete-orphan")
    
    user_communities_link = relationship("UserCommunity", back_populates="user", cascade="all, delete-orphan")
    community_posts = relationship("CommunityPost", back_populates="user", cascade="all, delete-orphan")
    post_likes = relationship("PostLike", back_populates="user", cascade="all, delete-orphan")
    post_comments = relationship("PostComment", back_populates="user", cascade="all, delete-orphan")