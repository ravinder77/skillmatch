from datetime import datetime, timedelta, timezone

from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import Integer, String, ForeignKey, Text, JSON, DateTime, func, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.enums import JobType
from app.models import EmployerProfile
from app.models.base import Base
from app.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Application, Company, User

class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    title:Mapped[str] = mapped_column(String(150), nullable=False, index=True) # candidates search job by name so index improves performance
    description:Mapped[str] = mapped_column(Text, nullable=False)
    skills_required:Mapped[list[str]] = mapped_column(JSON, nullable=False)
    experience_required:Mapped[int] = mapped_column(Integer, nullable=False)
    min_salary:Mapped[int] = mapped_column(Integer, nullable=False)
    max_salary:Mapped[int] = mapped_column(Integer, nullable=False)
    location:Mapped[Optional[str]]= mapped_column(String, nullable=True, index=True)
    is_active:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    job_type: Mapped[JobType] = mapped_column(Enum(JobType), default=JobType.FULL_TIME, nullable=False)

    posted_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc) + timedelta(days=30),
        nullable=True
    )
    # -- Foreign Keys --
    company_id:Mapped[int]= mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )
    employer_profile_id:Mapped[int] = mapped_column(
        ForeignKey("employer_profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationships
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="jobs"
    )
    employer_profile: Mapped["EmployerProfile"] = relationship(
        "EmployerProfile",
        back_populates="jobs"
    )
    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="job",
        cascade="all, delete-orphan"
    )
