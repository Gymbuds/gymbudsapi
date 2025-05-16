from app.db.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,Enum
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
import enum
class SkillLevel(enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
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
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    age = Column(Integer,nullable=True)
    skill_level = Column(Enum(SkillLevel), nullable=True)
    weight = Column(Integer,nullable=True)
    gender = Column(Enum(Gender),nullable=True)
    zip_code = Column(String,nullable=True)
    
    availability_ranges = relationship("AvailabilityRange", back_populates="user", cascade="all, delete-orphan") # if one user is deleted so are all of their ranges
    workout_logs = relationship("WorkoutLog", back_populates="user", cascade="all, delete-orphan")
    ai_advices = relationship("AIAdvice", back_populates="user", cascade="all, delete-orphan")
    health_datas = relationship("HealthData", back_populates="user", cascade="all, delete-orphan")
    
    user_communities_link = relationship("UserCommunity", back_populates="user", cascade="all, delete-orphan")
    community_posts = relationship("CommunityPost", back_populates="user", cascade="all, delete-orphan")
    post_likes = relationship("PostLike", back_populates="user", cascade="all, delete-orphan")
    post_comments = relationship("PostComment", back_populates="user", cascade="all, delete-orphan")

    match_results1 = relationship(
        "MatchResult",
        back_populates="user1",
        foreign_keys="[MatchResult.user_id1]",
        cascade="all, delete-orphan"
    )
    match_results2 = relationship(
        "MatchResult",
        back_populates="user2",
        foreign_keys="[MatchResult.user_id2]",
        cascade="all, delete-orphan"
    )
    candidates = relationship("MatchCandidate", foreign_keys="[MatchCandidate.user_id]", back_populates="user")
    is_candidate_of = relationship("MatchCandidate", foreign_keys="[MatchCandidate.candidate_user_id]", back_populates="candidate_user")

    match_preferences = relationship("MatchPreference",back_populates="user", cascade="all, delete-orphan")
    goals = relationship("UserGoal", back_populates="user", cascade="all, delete-orphan")
    user_chats_1 = relationship(
        "Chat",
        back_populates="user1",
        foreign_keys="[Chat.user_id1]",
        cascade="all, delete-orphan"
    )
    user_chats_2 = relationship(
        "Chat",
        back_populates="user2",
        foreign_keys="[Chat.user_id2]",
        cascade="all, delete-orphan"
    )
    sent_messages = relationship(
        "Message",
        back_populates="sender",
        cascade="all, delete-orphan"
    )