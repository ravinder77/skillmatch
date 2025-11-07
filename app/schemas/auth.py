from typing import Optional
from pydantic import BaseModel, ConfigDict
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

class LoginRequest(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

class Tokens(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

class AuthResponse(BaseModel):
    id: int
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


