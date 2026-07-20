"""
SQLAlchemy models for PathPilot AI.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    name = Column(String, nullable=False)
    career_goal = Column(String, nullable=False)
    skill_level = Column(String, nullable=False)
    hours_per_day = Column(Float, nullable=False)
    total_hours = Column(Float, nullable=False)
    source = Column(String, default="gemini")  # "gemini" or "template_fallback"
    created_at = Column(DateTime, default=datetime.utcnow)

    weeks = relationship(
        "RoadmapWeek", back_populates="roadmap",
        cascade="all, delete-orphan", order_by="RoadmapWeek.week_number"
    )


class RoadmapWeek(Base):
    __tablename__ = "roadmap_weeks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roadmap_id = Column(String, ForeignKey("roadmaps.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    resource_name = Column(String, nullable=False)
    resource_url = Column(String, nullable=False)
    project = Column(String, nullable=False)
    hours = Column(Float, nullable=False)

    roadmap = relationship("Roadmap", back_populates="weeks")
