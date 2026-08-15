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

## Deploy (GitHub + Render) — Recommended for now

We are using **GitHub for source** + **Render for hosting** (free tier friendly for Python/FastAPI).

### 1. Push to GitHub (first time)

```bash
# On your machine (you are here)
cd /Users/prince/socratic-edtech-platform

# Create a new repo on GitHub.com first (e.g. "socratic-edtech")
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/socratic-edtech.git
git branch -M main
git push -u origin main
```

### 2. Deploy Backend on Render (easiest)

1. Go to https://render.com → Sign up with GitHub
2. Click **"New +"** → **Web Service**
3. Connect your GitHub repo `socratic-edtech`
4. Render should auto-detect the `render.yaml` we added
5. Settings (Render will mostly fill these):
   - **Name**: socratic-edtech-backend (or anything)
   - **Environment**: Python 3
   - **Build Command**: (already in render.yaml)
   - **Start Command**: (already in render.yaml)
6. Click **Create Web Service**

Render will:
- Install requirements
- Run `bootstrap_db.py` (creates HK bilingual tables + demo data)
- Start the FastAPI server

Your backend will be live at something like:
`https://socratic-edtech-backend.onrender.com`

Visit `/docs` to see the API.

### 3. Later: Deploy Streamlit apps

You can add separate Render services for the Streamlit prototypes (student/teacher/parent) using the same repo.

For now the backend + API is the core.

### Notes
- SQLite on Render free tier is fine for prototypes (data resets on deploy sometimes).
- Later we can switch to Render Postgres (free) — just change DATABASE_URL.
- All HK bilingual fields (English + Cantonese) are already in the models and seed data.

Ready? Push to GitHub then hit deploy on Render.

## Your Live URL (after you deploy)

Once you push to GitHub and create the service on Render, your backend will be available at:

**https://socratic-edtech-backend.onrender.com**

- API docs: https://socratic-edtech-backend.onrender.com/docs
- Health: https://socratic-edtech-backend.onrender.com/health

The first deploy can take 2-5 minutes. 

