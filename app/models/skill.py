
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.testing.schema import mapped_column
from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.models.project import project_skills


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(50), nullable=False)
    description:Mapped[str] = mapped_column(Text, nullable=False)

    # user<-->skill link
    users = relationship("UserSkill", back_populates="skill")
    # Project <--> Skill link
    projects = relationship(
        "Project", secondary=project_skills, back_populates="skills"
    )
