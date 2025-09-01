from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import relationship
from app.db.base import Base

# curate which projects appear in the portfolio
featured_projects = Table(
    "featured_projects",
    Base.metadata,
    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "candidate_profile_id",
        Integer,
        ForeignKey("candidate_profile.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# Portfolio Model
class CandidateProfile(Base):
    __tablename__ = "candidate_profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # one-to-one relation with user
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    profile_image_url = Column(String, nullable=False)

    # Public Header Info
    headline = Column(String(160), nullable=True)
    summary = Column(String(1000), nullable=True)
    location = Column(String(120), nullable=True)
    education = Column(String(120), nullable=True)

    # Public Profile Urls
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)

    slug = Column(String(120), unique=True, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)

    # timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # relationship
    user = relationship("User", back_populates="profile", uselist=False)
    projects = relationship(
        "Project",
        secondary=featured_projects,
        backref="featured_in_projects",
        cascade="all",
    )
    applications = relationship("JobApplication", back_populates="candidate", cascade="all, delete-orphan")

