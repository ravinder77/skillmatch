from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserSkill(Base):
    __tablename__ = "user_skill"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)
    proficiency = Column(String, nullable=False)  # Beginner , Intermediate, Expert

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="users")
