from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    project_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)

    #relationship
    user = relationship("User", back_populates="portfolio")