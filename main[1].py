"""
PathPilot AI — backend API.

Endpoints:
  POST /api/generate           Generate a new personalized roadmap (Gemini-powered)
  GET  /api/roadmaps/{id}      Fetch a previously generated roadmap
  GET  /api/roadmaps           List roadmap history (optionally filter by ?name=)
  DELETE /api/roadmaps/{id}    Delete a roadmap
  GET  /health                 Health check
"""
import os
import logging

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
from schemas import RoadmapRequest, RoadmapOut, RoadmapSummary
from gemini_service import generate_roadmap_weeks

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PathPilot AI API",
    description="Backend for PathPilot AI — generates personalized learning roadmaps using Gemini.",
    version="1.0.0",
)

# Allow the Streamlit/frontend origin(s) to call this API.
# Set FRONTEND_ORIGINS to a comma-separated list in production, e.g.
# "https://pathpilot-ai-sri-hari1.vercel.app,http://localhost:8501"
origins_env = os.getenv("FRONTEND_ORIGINS", "*")
allow_origins = ["*"] if origins_env == "*" else [o.strip() for o in origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/generate", response_model=RoadmapOut)
def generate_roadmap(payload: RoadmapRequest, db: Session = Depends(get_db)):
    weeks_data, source = generate_roadmap_weeks(
        name=payload.name,
        career_goal=payload.career_goal,
        skill_level=payload.skill_level,
        hours_per_day=payload.hours_per_day,
    )

    total_hours = sum(w["hours"] for w in weeks_data)

    roadmap = models.Roadmap(
        name=payload.name,
        career_goal=payload.career_goal,
        skill_level=payload.skill_level,
        hours_per_day=payload.hours_per_day,
        total_hours=total_hours,
        source=source,
    )
    db.add(roadmap)
    db.flush()  # get roadmap.id before creating child rows

    for w in weeks_data:
        db.add(models.RoadmapWeek(
            roadmap_id=roadmap.id,
            week_number=w["week"],
            topic=w["topic"],
            resource_name=w["resource_name"],
            resource_url=w["resource_url"],
            project=w["project"],
            hours=w["hours"],
        ))

    db.commit()
    db.refresh(roadmap)

    return _to_roadmap_out(roadmap)


@app.get("/api/roadmaps/{roadmap_id}", response_model=RoadmapOut)
def get_roadmap(roadmap_id: str, db: Session = Depends(get_db)):
    roadmap = db.query(models.Roadmap).filter(models.Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return _to_roadmap_out(roadmap)


@app.get("/api/roadmaps", response_model=list[RoadmapSummary])
def list_roadmaps(
    name: str | None = Query(default=None, description="Filter by learner name"),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(models.Roadmap)
    if name:
        query = query.filter(models.Roadmap.name.ilike(f"%{name}%"))
    roadmaps = query.order_by(models.Roadmap.created_at.desc()).limit(limit).all()
    return roadmaps


@app.delete("/api/roadmaps/{roadmap_id}")
def delete_roadmap(roadmap_id: str, db: Session = Depends(get_db)):
    roadmap = db.query(models.Roadmap).filter(models.Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    db.delete(roadmap)
    db.commit()
    return {"deleted": roadmap_id}


def _to_roadmap_out(roadmap: models.Roadmap) -> RoadmapOut:
    return RoadmapOut(
        id=roadmap.id,
        name=roadmap.name,
        career_goal=roadmap.career_goal,
        skill_level=roadmap.skill_level,
        hours_per_day=roadmap.hours_per_day,
        total_hours=roadmap.total_hours,
        source=roadmap.source,
        created_at=roadmap.created_at,
        weeks=[
            {
                "week": w.week_number,
                "topic": w.topic,
                "resource_name": w.resource_name,
                "resource_url": w.resource_url,
                "project": w.project,
                "hours": w.hours,
            }
            for w in roadmap.weeks
        ],
    )
