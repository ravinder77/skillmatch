from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func, text
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.enums import UserRole
from app.db.base import Base
from app.db.mixins import TimestampMixin, SoftDeleteMixin


if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.application import JobApplication

# User Model
class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username:Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    first_name:Mapped[str] = mapped_column(String(50), nullable=False)
    last_name:Mapped[str] = mapped_column(String(50), nullable=False)
    email:Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    role:Mapped[UserRole] = mapped_column(
        Enum(UserRole, values_callable=lambda x:[e.value for e in x], native_enum=False),
        default=UserRole.CANDIDATE,
        nullable=False
    )
    hashed_password:Mapped[str] = mapped_column(String(255), nullable=False)

    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # Employer → Jobs
    jobs: Mapped[List["Job"]] = relationship(
        "Job",
        back_populates="employer",
        cascade="all, delete-orphan"
    )

    applications:Mapped[List["JobApplication"]] = relationship("JobApplication", back_populates="candidate")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, role={self.role})>"


