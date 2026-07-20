import os

import requests
import streamlit as st

# ── Backend config ───────────────────────────────────────────────────────────
# Point this at your deployed FastAPI backend (see backend/ folder).
# Locally this defaults to http://localhost:8000
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Learning Path Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.main-header {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
}
.main-header h1 {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
.main-header p {
    color: #64748b;
    font-size: 1.05rem;
}
.week-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s;
}
.week-card:hover {
    box-shadow: 0 4px 12px rgba(102,126,234,0.15);
}
.week-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    font-weight: 600;
    font-size: 0.8rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.5rem;
}
.week-topic {
    font-size: 1.15rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.75rem;
}
.section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #667eea;
    margin-bottom: 0.25rem;
}
.resource-item, .project-item {
    color: #475569;
    font-size: 0.9rem;
    padding: 0.15rem 0;
}
.summary-box {
    background: linear-gradient(135deg, #667eea15, #764ba215);
    border: 1px solid #667eea30;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
}
.summary-box h3 {
    color: #1e293b;
    margin-bottom: 0.5rem;
}
.summary-stat {
    display: inline-block;
    background: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin: 0.25rem 0.5rem 0.25rem 0;
    font-size: 0.85rem;
    color: #475569;
    border: 1px solid #e2e8f0;
}
.summary-stat strong {
    color: #667eea;
}
div[data-testid="stForm"] {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem;
}
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100%;
    transition: opacity 0.2s;
}
.stButton > button:hover {
    opacity: 0.9;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Backend call (with offline fallback) ─────────────────────────────────────
def call_backend(name: str, career_goal: str, skill_level: str, hours_per_day: float) -> tuple[dict | None, str | None]:
    """
    Calls the FastAPI backend's /api/generate endpoint.
    Returns (roadmap_json, error_message). error_message is None on success.
    """
    try:
        resp = requests.post(
            f"{BACKEND_URL}/api/generate",
            json={
                "name": name,
                "career_goal": career_goal,
                "skill_level": skill_level,
                "hours_per_day": hours_per_day,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.RequestException as exc:
        return None, str(exc)


# Local fallback generator, used only if the backend is completely unreachable
# (e.g. running the Streamlit app without the backend during development).
from fallback_templates import generate_template_roadmap  # noqa: E402


def render_week_card(week: dict) -> None:
    st.markdown(
        f"""
<div class="week-card">
    <div class="week-badge">Week {week['week']}</div>
    <div class="week-topic">{week['topic']}</div>
    <div class="section-label">📚 Free Resource</div>
    <div class="resource-item">
        <a href="{week['resource_url']}" target="_blank">{week['resource_name']}</a>
    </div>
    <div class="section-label" style="margin-top:0.75rem;">🛠️ Mini Project</div>
    <div class="project-item">{week['project']}</div>
    <div class="section-label" style="margin-top:0.75rem;">⏱️ Estimated Time</div>
    <div class="resource-item">~{week['hours']} hours this week</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="main-header">
    <h1>🎓 Learning Path Generator</h1>
    <p>Your personalized 12-week roadmap to career success — tailored to your goals, skills, and schedule.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Input form ───────────────────────────────────────────────────────────────
col_form, col_info = st.columns([1, 1], gap="large")

with col_form:
    with st.form("learning_path_form"):
        name = st.text_input("Your Name", placeholder="e.g. Alex Johnson")
        career_goal = st.text_input(
            "Career Goal",
            placeholder="e.g. Data Science, Web Development, Machine Learning",
        )
        skill_level = st.selectbox(
            "Current Skill Level",
            ["Beginner", "Intermediate", "Advanced"],
        )
        hours_per_day = st.number_input(
            "Study Hours Per Day",
            min_value=0.5,
            max_value=12.0,
            value=2.0,
            step=0.5,
        )
        submitted = st.form_submit_button("Generate Learning Path")

with col_info:
    st.markdown("### How it works")
    st.markdown(
        """
1. **Tell us about yourself** — name, career goal, and current skill level.
2. **Set your schedule** — how many hours you can study each day.
3. **Get your roadmap** — a structured 12-week plan with:
   - 📌 Weekly focus topics
   - 📚 Curated free learning resources
   - 🛠️ Hands-on mini projects
   - ⏱️ Time estimates based on your schedule
"""
    )
    st.info(
        "Roadmaps are generated by **Google Gemini**, tailored to any career goal you "
        "enter — not just a fixed list of paths."
    )

# ── Generate & display roadmap ───────────────────────────────────────────────
if submitted:
    if not name.strip():
        st.warning("Please enter your name.")
    elif not career_goal.strip():
        st.warning("Please enter your career goal.")
    else:
        with st.spinner("Generating your personalized roadmap..."):
            result, error = call_backend(name.strip(), career_goal.strip(), skill_level, hours_per_day)

        if result is not None:
            roadmap = result["weeks"]
            total_hours = result["total_hours"]
            source = result.get("source", "gemini")
        else:
            # Backend unreachable — fall back to local template generation so the
            # app still works, but let the user know.
            st.warning(
                f"Couldn't reach the backend at `{BACKEND_URL}` ({error}). "
                "Showing a locally generated roadmap instead."
            )
            roadmap = generate_template_roadmap(career_goal.strip(), skill_level, hours_per_day)
            total_hours = sum(w["hours"] for w in roadmap)
            source = "template_fallback"

        st.markdown("---")
        st.markdown(
            f"""
<div class="summary-box">
    <h3>👋 Hello, {name.strip()}!</h3>
    <p>Here's your personalized <strong>12-week learning path</strong> for
    <strong>{career_goal.strip()}</strong>.</p>
    <div>
        <span class="summary-stat">📊 Level: <strong>{skill_level}</strong></span>
        <span class="summary-stat">⏰ Daily: <strong>{hours_per_day} hrs</strong></span>
        <span class="summary-stat">📅 Total: <strong>~{total_hours:.0f} hrs</strong></span>
        <span class="summary-stat">🗓️ Duration: <strong>12 weeks</strong></span>
        <span class="summary-stat">✨ Source: <strong>{'Gemini AI' if source == 'gemini' else 'Template'}</strong></span>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("### 📋 Your 12-Week Roadmap")
        left_col, right_col = st.columns(2, gap="medium")
        for idx, week in enumerate(roadmap):
            with left_col if idx % 2 == 0 else right_col:
                render_week_card(week)

        st.markdown("---")
        st.success(
            f"🎉 Roadmap generated! Commit to {hours_per_day} hours/day and you'll "
            f"complete this path in 12 weeks. Good luck, {name.strip()}!"
        )

        st.download_button(
            label="📥 Download Roadmap as Text",
            data="\n\n".join(
                f"Week {w['week']}: {w['topic']}\n"
                f"  Resource: {w['resource_name']} ({w['resource_url']})\n"
                f"  Project: {w['project']}\n"
                f"  Hours: ~{w['hours']}"
                for w in roadmap
            ),
            file_name=f"learning_path_{name.strip().replace(' ', '_').lower()}.txt",
            mime="text/plain",
        )
