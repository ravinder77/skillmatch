from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.job_application import JobApplication


class Job(Base):
    __tablename__ = "jobs"
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(String, nullable=False, index=True) # candidates search job by name so index improves performance
    description:Mapped[str] = mapped_column(Text, nullable=False)
    skills_required:Mapped[List[str]] = mapped_column(JSON, nullable=False)
    experience_required:Mapped[int] = mapped_column(Integer, nullable=False)
    min_salary:Mapped[int] = mapped_column(Integer, nullable=False)
    max_salary:Mapped[int] = mapped_column(Integer, nullable=False)
    job_type:Mapped[str] = mapped_column(String, default="Full-Time") # Full-Time, Part-Time, Contract
    location:Mapped[Optional[str]]= mapped_column(String, nullable=True, index=True)
    is_active:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    posted_at:Mapped[datetime] = mapped_column( DateTime(timezone=True), server_default=func.now(), nullable=False)

    expires_at:Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now() + timedelta(days=30),
        nullable=True
    )

    employer_id:Mapped[int]= mapped_column(ForeignKey("users.id"), nullable=False)
    # Relationships
    applications:Mapped[List["JobApplication"]] = relationship("JobApplication", back_populates="job")


