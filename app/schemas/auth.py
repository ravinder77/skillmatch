from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional


# =========
# User Role
# =========
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    EMPLOYER = "employer"


# Request schema for Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Response schema for JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class AuthResponse(BaseModel):
    id: str
    username: str
    email: str
    access_token: str
    token_type: str = "bearer"


    class Config:
        from_attributes = True