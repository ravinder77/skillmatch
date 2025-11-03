from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    description: str
    skills_required: List[str]
    experience_required: int
    min_salary: int
    max_salary: int
    location: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    skills_required: Optional[List[str]]
    experience_required: Optional[int]
    min_salary: Optional[int]
    max_salary: Optional[int]
    location: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    skills_required: List[str]
    experience_required: int
    min_salary: int
    max_salary: int
    location: Optional[str]
    employer_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )
