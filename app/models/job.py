from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base



class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    skills_required = Column(JSON, nullable=False)
    experience_required = Column(Integer, nullable=False)
    location = Column(String, nullable=True)
    employer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # employer
    employer = relationship("User")
