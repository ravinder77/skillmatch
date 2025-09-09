from datetime import datetime

from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional, List
from app.core.enums import ApplicationStatus


class CandidateProfileCreate(BaseModel):
    profile_image_url: Optional[str]
    headline: Optional[str]
    summary: Optional[str]
    education: Optional[str]
    location: Optional[str]

    github_url: Optional[HttpUrl]
    linkedin_url: Optional[HttpUrl]
    is_public: Optional[bool] = True

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        from_attributes=True,
    )

class CandidateProfileUpdate(BaseModel):
    profile_image_url: Optional[HttpUrl]
    headline: Optional[str]
    summary: Optional[str]
    education: Optional[str]
    location: Optional[str]

    github_url: Optional[HttpUrl]
    linkedin_url: Optional[HttpUrl]
    is_public: Optional[bool] = True

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


class CandidateProfileResponse(BaseModel):
    id: int
    profile_image_url: Optional[str]
    headline: Optional[str]
    summary: Optional[str]
    education: Optional[str]
    location: Optional[str]
    github_url: Optional[HttpUrl]
    linkedin_url: Optional[HttpUrl]
    slug: str
    is_public: bool


    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        validate_by_alias=True,

    )


class CandidateProfilePublicView(BaseModel):
    id: int
    profile_image_url: Optional[str]
    headline: Optional[str]
    summary: Optional[str]
    education: Optional[str]
    location: Optional[str]
    github_url: Optional[HttpUrl]
    linkedin_url: Optional[HttpUrl]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

