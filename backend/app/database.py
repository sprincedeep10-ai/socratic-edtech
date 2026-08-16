from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Deploy-friendly DB path
# - On Render (/opt/render exists): use /tmp (writable)
# - Locally: resolve to project_root/data/socratic.db
#   (works whether cwd is project root or backend/ or running via uvicorn)
if os.path.exists("/opt/render"):
    DB_DIR = "/tmp"
else:
    # From backend/app/database.py -> parent x3 = project root
    here = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    DB_DIR = os.path.join(project_root, "data")

os.makedirs(DB_DIR, exist_ok=True)
DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'socratic.db')}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
