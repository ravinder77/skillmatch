import enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.core.enums import UserRole


# Request schema for Login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)


# Response schema for JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class AuthResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: Optional[UserRole] = None
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True
