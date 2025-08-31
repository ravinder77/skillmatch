from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict

from app.core.enums import ApplicationStatus


class JobApplicationCreate(BaseModel):
    status: ApplicationStatus
    resume_url: Optional[HttpUrl] = None

    model_config = ConfigDict(
        from_attributes= True,
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )