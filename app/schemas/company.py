from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator


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
        extra="forbid",
    )


class CompanyCreate(BaseModel):
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
        extra="forbid",
    )


class CompanyUpdate(BaseModel):
    name: str
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
        extra="forbid",
    )


class CompanyResponse(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
    size: Optional[str] = None
    industry: Optional[str] = None
