from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict


class PortfolioCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )


class PortfolioUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )