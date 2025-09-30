from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.testing.schema import mapped_column

from app.db.base import Base


class UserSkill(Base):
    __tablename__ = "user_skill"
    user_id:Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id:Mapped[int] = mapped_column(Integer, ForeignKey("skills.id"), primary_key=True)
    proficiency:Mapped[str] = mapped_column(String(50), nullable=False)  # Beginner , Intermediate, Expert

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="users")
