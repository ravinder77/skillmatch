from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    skills = Column(JSON, nullable=False)
    experience = Column(Integer, nullable=False)
    resume_text = Column(Text, nullable=True)

    #relationship
    user = relationship("User")

