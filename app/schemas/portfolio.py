from typing import Optional

from pydantic import BaseModel, HttpUrl


class PortfolioCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None


class PortfolioUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

    class Config:
        from_attributes = True
