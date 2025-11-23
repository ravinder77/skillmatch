from sqlalchemy import  String, Integer, ForeignKey, Enum, DateTime, func
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime

from app.db.mixins import TimestampMixin
from app.models.base import Base
from app.core.enums import ApplicationStatus

if TYPE_CHECKING:
    from app.models import Job, User


class Application(Base, TimestampMixin):
    """
       Represents a job application submitted by a user (candidate)
       for a particular job posting.
       """
    __tablename__ = 'applications'
    # foreign keys
    applicant_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False
    )
    job_id: Mapped[int] = mapped_column(
        ForeignKey('jobs.id', ondelete="CASCADE"),
        nullable=False
    )
    # application_status
    status:Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, values_callable=lambda x:[e.value for e in x], native_enum=False),
        default=ApplicationStatus.APPLIED,
        nullable=False
    )
    # application content
    cover_letter: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    resume_url:Mapped[Optional[str]] = mapped_column(String, nullable=True)


    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    #relationships
    applicant: Mapped["User"] = relationship("User", back_populates="applications")
    job: Mapped["Job"] = relationship("Job", back_populates="applications")






