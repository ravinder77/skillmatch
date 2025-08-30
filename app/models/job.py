from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base



class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True) # candidates search job by name so index improves performance
    description = Column(Text, nullable=False)
    skills_required = Column(JSON, nullable=False)
    experience_required = Column(Integer, nullable=False)
    min_salary = Column(Integer, nullable=False)
    max_salary = Column(Integer, nullable=False)
    job_type = Column(String, default="Full-Time") # Full-Time, Part-Time, Contract
    location = Column(String, nullable=True, index=True)

    posted_at = Column( DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column( DateTime(timezone=True), nullable=True, server_default=func.now())

    # Relation
    employer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employer = relationship("User", back_populates="jobs")

