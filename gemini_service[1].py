"""
Gemini AI integration for PathPilot AI.

Calls Google's Gemini API to generate a genuinely personalized 12-week
roadmap (rather than picking from a fixed template). Falls back to the
offline template generator in fallback_templates.py if:
  - GEMINI_API_KEY isn't set, or
  - the Gemini call fails or returns something we can't parse.
"""
import json
import logging
import os

import google.generativeai as genai

from fallback_templates import generate_template_roadmap

logger = logging.getLogger("pathpilot.gemini")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# JSON schema Gemini must conform to. Keeps the response predictable
# enough to store directly in the database.
ROADMAP_SCHEMA = {
    "type": "object",
    "properties": {
        "weeks": {
            "type": "array",
            "minItems": 12,
            "maxItems": 12,
            "items": {
                "type": "object",
                "properties": {
                    "week": {"type": "integer"},
                    "topic": {"type": "string"},
                    "resource_name": {"type": "string"},
                    "resource_url": {"type": "string"},
                    "project": {"type": "string"},
                    "hours": {"type": "number"},
                },
                "required": ["week", "topic", "resource_name", "resource_url", "project", "hours"],
            },
        }
    },
    "required": ["weeks"],
}


def _build_prompt(name: str, career_goal: str, skill_level: str, hours_per_day: float) -> str:
    weekly_hours = round(hours_per_day * 7, 1)
    return f"""You are an expert career coach and curriculum designer.

Create a personalized 12-week learning roadmap for the following learner:
- Name: {name}
- Career goal: {career_goal}
- Current skill level: {skill_level}
- Available study time: {hours_per_day} hours/day (~{weekly_hours} hours/week)

Requirements for each of the 12 weeks:
- A specific, non-generic weekly topic that builds logically on the previous week
- One genuinely useful, currently-free learning resource (real, working URL — prefer official docs, freeCodeCamp, Coursera audit, Kaggle Learn, MDN, YouTube channels, etc.)
- One concrete hands-on mini project scoped to that week
- An "hours" estimate for that week, scaled to the learner's available time and skill level (experienced learners move faster, beginners need more time on fundamentals)

Tailor difficulty and pacing to the stated skill level, and tailor topics specifically to "{career_goal}" rather than a generic tech curriculum.

Return ONLY valid JSON matching this exact shape, nothing else:
{{
  "weeks": [
    {{
      "week": 1,
      "topic": "...",
      "resource_name": "...",
      "resource_url": "https://...",
      "project": "...",
      "hours": 10.5
    }}
    // ... total of 12 week objects
  ]
}}"""


def generate_roadmap_weeks(name: str, career_goal: str, skill_level: str, hours_per_day: float) -> tuple[list[dict], str]:
    """
    Returns (weeks, source) where source is "gemini" or "template_fallback".
    """
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set — using template fallback")
        return generate_template_roadmap(career_goal, skill_level, hours_per_day), "template_fallback"

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        prompt = _build_prompt(name, career_goal, skill_level, hours_per_day)

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=ROADMAP_SCHEMA,
                temperature=0.7,
            ),
        )

        data = json.loads(response.text)
        weeks = data["weeks"]

        if len(weeks) != 12:
            raise ValueError(f"Expected 12 weeks, got {len(weeks)}")

        weeks.sort(key=lambda w: w["week"])
        return weeks, "gemini"

    except Exception as exc:  # noqa: BLE001 — any failure should fall back, not 500
        logger.error("Gemini generation failed, using template fallback: %s", exc)
        return generate_template_roadmap(career_goal, skill_level, hours_per_day), "template_fallback"
