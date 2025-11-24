from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import UserRole
from app.db.mixins import SoftDeleteMixin, TimestampMixin
from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Application, Company, EmployerProfile, Job


# User Model
class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole, values_callable=lambda x: [e.value for e in x], native_enum=False
        ),
        default=UserRole.APPLICANT,
        nullable=False,
    )
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # user may have employer profile
    employer_profile: Mapped["EmployerProfile"] = relationship(
        "EmployerProfile",
        back_populates="user",
        uselist=False,
    )

    # applications
    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="applicant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, role={self.role})>"
