from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional,List
from app.db.base import Base
from app.models.candidate_profile import CandidateProfile
from app.models.skill import Skill
from app.models.user import User
from app.core.enums import ProjectStatus
from app.db.mixins import TimestampMixin, SoftDeleteMixin

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
class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title:Mapped[str] = mapped_column(String(100), nullable=False)
    description:Mapped[str] = mapped_column(Text, nullable=False)

    status:Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, values_callable=lambda x:[e.value for e in x], native_enum=False),
        default=ProjectStatus.IN_PROGRESS,
        nullable=False
    )
    github_url:Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    demo_url:Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url:Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    user:Mapped["User"] = relationship("User", back_populates="projects")
    #foreign key to Candidate Profile
    candidate_profile_id:Mapped[int] = mapped_column(
        Integer, ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    # relationship back to candidate Profile
    candidate_profile:Mapped["CandidateProfile"] = relationship(
        "CandidateProfile",
        back_populates="projects",
    )
    # one to many with skills
    skills:Mapped[List["Skill"]] = relationship("Skill", secondary=project_skills, back_populates="projects")
