from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Column
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserSkill(Base):
    __tablename__ = 'user_skill'
    user_id = Column(Integer, ForeignKey('user.id'))
    skill_id = Column(Integer, ForeignKey('skill.id'))
    proficiency = Column(String)  # Beginner , Intermediate, Expert

    user = relationship('User', back_populates='skills')
    skill = relationship('Skill', back_populates='users')