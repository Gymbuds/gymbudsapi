from pydantic import BaseModel, EmailStr

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

