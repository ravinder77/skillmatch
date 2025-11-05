from datetime import datetime

from sqlalchemy import Boolean, Enum, Integer, String, Text, DateTime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.enums import UserRole
from app.models.base import Base
from app.db.mixins import TimestampMixin, SoftDeleteMixin


if TYPE_CHECKING:
    from app.models import Job, Company, Application


# User Model
class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    first_name:Mapped[str] = mapped_column(String(50), nullable=False)
    last_name:Mapped[str] = mapped_column(String(50), nullable=False)
    email:Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password:Mapped[str] = mapped_column(String(255), nullable=False)

    role:Mapped[UserRole] = mapped_column(
        Enum(UserRole, values_callable=lambda x:[e.value for e in x], native_enum=False),
        default=UserRole.CANDIDATE,
        nullable=False
    )

    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships , user can create multiple companies
    companies: Mapped[List["Company"]] = relationship(
        "Company",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # jobs
    jobs: Mapped[List["Job"]] = relationship(
        "Job",
        back_populates="employer",
        cascade="all, delete-orphan"
    )
    # applications
    applications:Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="candidate",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, role={self.role})>"


