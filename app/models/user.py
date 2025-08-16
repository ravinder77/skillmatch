from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.enums import UserRole
from app.db.base import Base


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relationships
    # one-to-many relation with skills, a user can have many skills
    skills = relationship(
        "UserSkill", back_populates="user", cascade="all, delete-orphan"
    )

    # one-to-many relation with projects, a user can have many projects
    projects = relationship(
        "Project", back_populates="user", cascade="all, delete-orphan"
    )
    portfolio = relationship(
        "Portfolio", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
