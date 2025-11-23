from typing import TYPE_CHECKING

from sqlalchemy import Column,ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import EmployerRole
from app.models.base import Base

if TYPE_CHECKING:
    from app.models import User, Company, Job

class EmployerProfile(Base):
    __tablename__ = "employer_profiles"


    user_id = mapped_column( ForeignKey("users.id"), nullable=False)
    company_id = mapped_column(ForeignKey("companies.id"), nullable=False)
    role: Mapped[EmployerRole] = mapped_column(
        Enum(EmployerRole),
        default=EmployerRole.ADMIN,
        nullable=False,
    )

    # Relationship
    user: Mapped["User"] = relationship(User, back_populates="employer_profile")
    company: Mapped["Company"] = relationship(Company, back_populates="employer_profiles")
    jobs: Mapped["Job"] = relationship(Job, back_populates="employer_profile")



