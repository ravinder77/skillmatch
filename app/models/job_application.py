from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from app.db.base import Base
from app.core.enums import ApplicationStatus
from app.models.job import Job
from app.models.candidate_profile import CandidateProfile


class JobApplication(Base):
    __tablename__ = 'job_application'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id:Mapped[int] = mapped_column(Integer, ForeignKey('candidate_profile.id'), nullable=False)
    job_id:Mapped[int] = mapped_column(Integer, ForeignKey('jobs.id'), nullable=False)

    status:Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, values_callable=lambda x:[e.value for e in x], native_enum=False),
        default=ApplicationStatus.APPLIED,
        nullable=False
    )
    resume_url:Mapped[str] = mapped_column(String, nullable=False)
    applied_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    #relationships
    job:Mapped["Job"] = relationship("Job", back_populates="applications")
    candidate:Mapped["CandidateProfile"] = relationship("CandidateProfile", back_populates="applications")






