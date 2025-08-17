from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from app.core.enums import ProjectStatus



class ProjectCreate(BaseModel):
    title: str
    description: str
    status: ProjectStatus = ProjectStatus.IN_PROGRESS
    github_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    skills_id: Optional[List[int]] = []


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    skills_id: Optional[List[int]] = []


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


    class Config:
        from_attributes = True
