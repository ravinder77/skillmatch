from typing import TYPE_CHECKING, List

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.mixins import TimestampMixin
from app.models.base import Base

if TYPE_CHECKING:
    from app.models import EmployerProfile, Job, User


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    website: Mapped[str] = mapped_column(String(255), nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[str] = mapped_column(String(255), nullable=True)
    size: Mapped[str] = mapped_column(String(50), nullable=True)
    industry: Mapped[str] = mapped_column(String(100), nullable=True)

    # relationships
    # Many employer_profiles can be tied to a company
    employer_profiles: Mapped[List["EmployerProfile"]] = relationship(
        "EmployerProfile", back_populates="company", cascade="all, delete-orphan"
    )
    # multiple jobs belong to one company
    jobs: Mapped[List["Job"]] = relationship(
        "Job", back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Company=({self.name})>"
