
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from typing import Optional, List
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from app.models.job_application import JobApplication
from app.models.user import User
from app.db.mixins import TimestampMixin
from app.models.project import Project


# Portfolio Model
class CandidateProfile(Base, TimestampMixin):
    __tablename__ = "candidate_profile"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # one-to-one relation with user
    user_id:Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Public Header Info
    headline:Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    summary:Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    location:Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    education:Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    # Urls
    profile_image_url:Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    github_url:Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url:Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    slug:Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_public:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # relationship
    # one-to-one: a user can have only one profile
    user:Mapped["User"] = relationship("User", back_populates="profile", uselist=False)
    #one-to-many: a candidate can have many projects
    projects:Mapped[List["Project"]] = relationship(
        "Project",
        back_populates="candidate_profile",
        cascade="all, delete-orphan",
    )
    applications:Mapped[List["JobApplication"]] = relationship("JobApplication", back_populates="candidate", cascade="all, delete-orphan")

