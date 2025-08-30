from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func
)

from sqlalchemy.orm import relationship
from app.db.base import Base
from app.core.enums import ProjectStatus


# Association table for Many-to-Many (Projects <--> Skills)
project_skills = Table(
    "project_skills",
    Base.metadata,
    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    ),
)


# Project Model
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(ProjectStatus, values_callable=lambda x:[e.value for e in x]), default=ProjectStatus.IN_PROGRESS.value, nullable=False)
    github_url = Column(Text, nullable=True)
    demo_url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    # Relationship
    user = relationship("User", back_populates="projects")
    skills = relationship("Skill", secondary=project_skills, back_populates="projects")
