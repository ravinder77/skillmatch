from typing import Optional
from pydantic import BaseModel, HttpUrl, ConfigDict


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    location: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    size: Optional[str] = None
    industry: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        extra='forbid',
    )

class CompanyCreate(CompanyBase):
    owner_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid',
        validate_by_name=True,
    )

class CompanyUpdate(BaseModel):
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    location: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
    size: Optional[str] = None
    industry: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        extra='forbid',
    )

