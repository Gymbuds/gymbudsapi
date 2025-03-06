from pydantic import BaseModel, EmailStr

# User registration schema 
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
