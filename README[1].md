# PathPilot AI — Backend

A FastAPI backend for PathPilot AI. It replaces the old hardcoded-template
logic with real **Google Gemini** calls and persists every generated
roadmap to a database so it can be revisited later.

## What it does

- `POST /api/generate` — takes `{name, career_goal, skill_level, hours_per_day}`,
  asks Gemini to generate a genuinely personalized 12-week roadmap (topics,
  free resources, mini projects, time estimates), saves it, and returns it.
- `GET /api/roadmaps/{id}` — fetch a previously generated roadmap by ID.
- `GET /api/roadmaps?name=...` — list roadmap history, optionally filtered by learner name.
- `DELETE /api/roadmaps/{id}` — delete a stored roadmap.
- `GET /health` — health check.

If `GEMINI_API_KEY` isn't set, or the Gemini call fails for any reason, the
API automatically falls back to the original hardcoded templates so it
never hard-fails — the response just includes `"source": "template_fallback"`
instead of `"source": "gemini"`.

## Local setup

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and set GEMINI_API_KEY (get one free at https://aistudio.google.com/apikey)

uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for interactive API docs (Swagger UI).

## Database

Uses SQLite by default (`pathpilot.db`, created automatically — nothing to
configure). To use Postgres instead, set `DATABASE_URL` in `.env`, e.g.:

```
DATABASE_URL=postgresql://user:password@host:5432/pathpilot
```

## Deploying

This is a standard FastAPI app, so it deploys anywhere that runs Python —
**Render**, **Railway**, **Fly.io**, or a VM are the easiest options (Vercel's
serverless functions aren't a great fit for a stateful Streamlit-adjacent API
with a persistent SQLite file — use Postgres there if you go that route).

Example (Render / Railway):
1. Push this repo to GitHub.
2. Create a new "Web Service", point it at the `backend/` folder.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Set env vars: `GEMINI_API_KEY`, `FRONTEND_ORIGINS` (your Streamlit app's URL), and `DATABASE_URL` if using Postgres.

Once deployed, set `BACKEND_URL` in your Streamlit app's environment to the
deployed backend's URL (e.g. `https://pathpilot-backend.onrender.com`).

## Project structure

```
backend/
├── main.py               FastAPI app & routes
├── database.py            SQLAlchemy engine/session setup
├── models.py               DB models (Roadmap, RoadmapWeek)
├── schemas.py               Pydantic request/response models
├── gemini_service.py         Gemini API call + JSON schema
├── fallback_templates.py      Offline template generator (safety net)
├── requirements.txt
└── .env.example
```
