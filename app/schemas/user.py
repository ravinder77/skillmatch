from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import UserRole


# Shared attributes
class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    bio: Optional[str] = None
    location: Optional[str] = None
    role: UserRole = UserRole.APPLICANT


# ===========
# Create User Schema
# ===========
class UserCreate(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=3, max_length=32)
    password: str = Field(
        min_length=7,
        max_length=256,
    )
    role: Optional[UserRole] = UserRole.APPLICANT
    bio: Optional[str] = None
    location: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        use_enum_values=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


# ============
# Update User Schema
# ============
class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=3, max_length=32)
    last_name: Optional[str] = Field(None, min_length=3, max_length=32)
    bio: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
    )


# ===========
# User Response
# ==========
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        use_enum_values=True,
    )
