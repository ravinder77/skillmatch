from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from app.core.enums import ProjectStatus



class ProjectCreate(BaseModel):
    title: str
    description: str
    status: ProjectStatus = ProjectStatus.IN_PROGRESS
    github_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    skills_id: Optional[List[int]] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True
    )


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    skills_id: Optional[List[int]] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True
    )


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: ProjectStatus = ProjectStatus.IN_PROGRESS
    github_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    skills_id: Optional[List[int]] = []

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True
    )
