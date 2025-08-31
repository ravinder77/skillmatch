from sqlalchemy import Column, String, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.core.enums import ApplicationStatus

class JobApplication(Base):
    __tablename__ = 'job_application'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidate_profile.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    status = Column(Enum(ApplicationStatus, values_callable=lambda x:[e.value for e in x]), default=ApplicationStatus.APPLIED.value, nullable=False)
    resume_url= Column(String, nullable=False)
    applied_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    #relationships
    job = relationship("Job", back_populates="applications")
    candidate = relationship("CandidateProfile", back_populates="applications")




