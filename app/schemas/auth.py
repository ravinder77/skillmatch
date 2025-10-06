import enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.core.enums import UserRole



# Response schema for JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )


class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )


class AuthResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: Optional[UserRole] = None
    access_token: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )
