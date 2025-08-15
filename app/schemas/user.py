from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from app.core.enums import UserRole

# ===========
# Create User Schema
# ===========
class UserCreate(BaseModel):
    username: str = Field(min_length=7, max_length=32)
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=64) #plain text hashed before saving
    role: Optional[UserRole] = UserRole.USER


# ============
# Update User Schema
# ============
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=32)
    first_name: Optional[str] = Field(None, min_length=3, max_length=32)
    last_name: Optional[str] = Field(None, min_length=3, max_length=32)
    password: Optional[str] = Field(None, min_length=8, max_length=64)
    is_active: Optional[bool] = None


#===========
# User Response
# ==========
class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: Optional[bool] = None


    class Config:
        from_attributes = True
