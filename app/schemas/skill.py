from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class SkillCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=255)

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=255)

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )


class SkillResponse(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=255)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
    )
