from typing import Optional, List
from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    description: str
    skill_required: List[str]
    experience_required: int
    location_required: Optional[str]


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    skills_required: Optional[List[str]]
    experience_required: Optional[int]
    location: Optional[str]


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    skills_required: List[str]
    experience_required: int
    location: Optional[str]
    employer_id: int

    class Config:
        from_attributes = True