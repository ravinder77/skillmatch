from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.db.base import Base

# curate which projects appear in the portfolio
portfolio_featured_projects = Table(
    "portfolio_featured_projects",
    Base.metadata,
    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "portfolio_id",
        Integer,
        ForeignKey("portfolio.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# Portfolio Model
class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # one-to-one relation with user
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Public Header Info
    headline = Column(String(160), nullable=True)
    summary = Column(String(1000), nullable=True)
    location = Column(String(120), nullable=True)

    # Public Profile Urls
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)

    slug = Column(String(120), unique=True, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)

    # timestamps
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    # relationship
    user = relationship("User", back_populates="portfolio", uselist=False)
    featured_projects = relationship(
        "Project",
        secondary=portfolio_featured_projects,
        backref="featured_in_projects",
        cascade="all",
    )
