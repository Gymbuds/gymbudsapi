from pydantic import BaseModel, EmailStr

# User registration schema 
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User login schema 
class UserLogin(BaseModel):
    email: EmailStr
    password: str
