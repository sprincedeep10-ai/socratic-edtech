# SocraticEd — Multi-Interface EdTech Platform

**Acted as:** World-class Full-Stack EdTech Architect

## Vision
A platform with three tightly integrated interfaces:

1. **Student Chat** — Gamified Socratic dialogue with real-time cognitive bottleneck tagging.
2. **Teacher Dashboard** — Deep learning-gap analytics + zero-click recommended actions.
3. **Parent Companion** — Plain-language summaries + micro-actions.

## Tech Stack (Foundational)
- **Backend**: Python + FastAPI
- **Database**: SQLite (easy start) → easily swappable for PostgreSQL
- **ORM**: SQLAlchemy
- **Prototypes**: Streamlit (lightweight, fast iteration)
- **Future**: Can evolve to Next.js/React frontends + Postgres

## Master Directory Tree

```
socratic-edtech-platform/
├── README.md
├── .env.example
├── docker-compose.yml (future)
│
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py                 # FastAPI entrypoint
│   │   ├── database.py
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── schemas.py              # Pydantic models
│   │   ├── crud.py                 # Data access layer
│   │   └── routers/
│   │       ├── chat.py             # Student chat + tagging
│   │       ├── analytics.py        # Teacher analytics
│   │       └── summaries.py        # Parent summaries
│   └── init_db.py
│
├── apps/
│   ├── student/
│   │   └── app.py                  # Streamlit: Gamified Socratic chat
│   ├── teacher/
│   │   └── app.py                  # Streamlit: Learning gap dashboard
│   └── parent/
│       └── app.py                  # Streamlit: Plain-language companion
│
├── shared/
│   └── seed.py                     # Seed realistic demo data
│
├── scripts/
│   └── run_all.py                  # Convenience launcher
│
└── data/
    └── socratic.db                 # SQLite database (gitignored)
```

## Quick Start

```bash
cd socratic-edtech-platform

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate     # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python init_db.py             # creates tables + seeds demo data

# Run API
uvicorn app.main:app --reload

# In new terminals:
cd apps/student && streamlit run app.py
cd apps/teacher && streamlit run app.py
cd apps/parent && streamlit run app.py
```

## Core Concepts (Boilerplate)

- **CognitiveBottleneck**: Tags like `conceptual_misunderstanding`, `procedural_gap`, `attention_fragmentation`, `prior_knowledge`.
- **SocraticTurn**: Every message in chat has a `socratic_strategy` and optional `bottleneck_tags`.
- **LearningGap**: Aggregated insights per student → teacher sees heatmaps + zero-click prompts.
- **ParentSummary**: LLM-ready plain language + 1-2 micro-actions.

This boilerplate gives you:
- Working FastAPI with role-based routers
- SQLite schema + seed data
- Three runnable Streamlit prototypes connected to the same backend
- Clean separation for future scaling

---

Ready for the next layer: real LLM integration, gamification engine, advanced analytics, auth, etc.
