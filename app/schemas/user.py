from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional


# ===========
# Shared User Field
# ===========
class UserBase(BaseModel):
    username: str = Field(min_length=7, max_length=32)
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=4, max_length=32)
    is_active: bool = Field(default=True)


# ===========
# Create User Schema
# ===========
class UserCreate(BaseModel):
    username: str = Field(min_length=7, max_length=32)
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=4, max_length=32)
    password: str = Field(min_length=8, max_length=64) #plain text hashed before saving


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
class UserResponse(UserBase):
    id: int


    class Config:
        from_attributes = True
