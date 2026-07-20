"""
Pydantic schemas for PathPilot AI backend.
"""
from datetime import datetime
from typing import Literal, List, Optional

from pydantic import BaseModel, Field


class RoadmapRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    career_goal: str = Field(..., min_length=1, max_length=200)
    skill_level: Literal["Beginner", "Intermediate", "Advanced"]
    hours_per_day: float = Field(..., ge=0.5, le=12.0)


class WeekOut(BaseModel):
    week: int
    topic: str
    resource_name: str
    resource_url: str
    project: str
    hours: float

    class Config:
        from_attributes = True


class RoadmapOut(BaseModel):
    id: str
    name: str
    career_goal: str
    skill_level: str
    hours_per_day: float
    total_hours: float
    source: str
    created_at: datetime
    weeks: List[WeekOut]

    class Config:
        from_attributes = True


class RoadmapSummary(BaseModel):
    id: str
    name: str
    career_goal: str
    skill_level: str
    created_at: datetime

    class Config:
        from_attributes = True
