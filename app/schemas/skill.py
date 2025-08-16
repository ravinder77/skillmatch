from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SkillCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=255)


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=255)


class SkillResponse(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=255)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
