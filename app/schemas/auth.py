from pydantic import BaseModel, ConfigDict




class LoginRequest(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    )

class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
