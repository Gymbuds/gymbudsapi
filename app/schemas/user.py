from pydantic import BaseModel, EmailStr
from app.db.models.user import SkillLevel
# Schema for user registration
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Schema for login request
class Login(BaseModel):
    email: EmailStr
    password: str

# Schema for refresh token request
class RefreshToken(BaseModel):
    refresh_token: str

# Schema for requesting password reset
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Schema for resetting password
class ResetPassword(BaseModel):
    reset_token: str
    new_password: str
class AuthToken(BaseModel):
    auth_token:str
class UserUpdate(BaseModel):
    name: str | None = None
    profile_picture: str | None = None
    preferred_workout_goals: str | None = None
    age: int | None = None 
    skill_level: str | None = None 
    weight: int | None = None
    gender: str | None = None
