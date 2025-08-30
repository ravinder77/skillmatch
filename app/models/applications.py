from sqlalchemy import Column, String, Integer, ForeignKey, Enum

from app.db.base import Base
from app.core.enums import ApplicationStatus

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidate_profile.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, nullable=False)




