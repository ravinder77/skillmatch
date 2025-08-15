import enum

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text, Table, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import enum



# Project Status Enum
class ProjectStatus(enum.Enum):
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    PLANNED = "Planned"


# Association table for Many-to-Many (Projects <--> Skills)
project_skills = Table(
    'project_skills',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
    Column('skill_id', Integer, ForeignKey('skills.id', ondelete='CASCADE'), nullable=False),
)


# Project Model
class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.IN_PROGRESS)

    github_url = Column(Text, nullable=True)
    demo_url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)

    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    # Relationship
    user = relationship('User', back_populates='projects')
    skills = relationship('Skill', secondary=project_skills, back_populates='projects')




