from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from app.core.enums import JobType


class JobCreate(BaseModel):
    title: str
    description: str
    skills_required: List[str]
    experience_required: int
    job_type: Optional[JobType]
    min_salary: int
    max_salary: int
    min_salary: int
    max_salary: int
    location: Optional[str]
    company_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    skills_required: Optional[List[str]]
    experience_required: Optional[int]
    job_type: Optional[JobType]
    min_salary: Optional[int]
    max_salary: Optional[int]
    location: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    skills_required: List[str]
    experience_required: int
    job_type: Optional[JobType]
    min_salary: int
    max_salary: int
    location: Optional[str]
    employer_id: int
    company_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )
