# StudyPlanner.agent — Autonomous Learning Planner

Hackathon-ready prototype for **Track 2: Education / Problem Statement 3**.

## What it demonstrates
A genuine agent loop, not just timetable generation:

1. **Observe** synthetic student performance and calendar state
2. **Diagnose** knowledge gaps and priorities
3. **Retrieve** matching resources from a local educational knowledge base
4. **Plan** sessions around availability and deadlines
5. **Track** completion/missed sessions and quiz scores
6. **Reassess** mastery after every event
7. **Replan** when time, performance or constraints change
8. **Verify** that the revised plan still satisfies learning/time objectives

## Fastest demo (no Node.js, no API key)
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Open `http://127.0.0.1:8000`.

## Groq + LangGraph
The prototype works fully in deterministic local mode. To enable optional LLM explanations:
```bash
set GROQ_API_KEY=your_key              # Windows CMD
export GROQ_API_KEY=your_key           # macOS/Linux
```
`backend/agent.py` contains the LangGraph state machine. The deterministic policy remains available as a safe fallback for hackathon demos.

## Suggested 3-minute demo
1. Open dashboard: explain agent state + priority gaps.
2. Click **Run Agent Cycle**: observe → diagnose → retrieve → plan → verify.
3. Mark a future session **Missed**: show automatic replan and conflict explanation.
4. Add a new blocked time: show schedule adapting.
5. Open Progress: show knowledge-gap coverage changing.
6. Open Agent Trace: prove the workflow is autonomous and tool-driven.

## Repository structure
- `backend/main.py` — FastAPI API + demo state
- `backend/agent.py` — LangGraph agent workflow
- `backend/models.py` — data models
- `backend/resources.py` — local educational RAG-style resource store
- `frontend/index.html` — standalone responsive UI (no npm required)
- `frontend/app.js` — interactions and API integration
- `frontend/styles.css` — UI inspired by the supplied reference
