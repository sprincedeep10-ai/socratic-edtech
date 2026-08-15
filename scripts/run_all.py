#!/usr/bin/env python3
"""One-command launcher for development (opens multiple processes)."""
import subprocess
import sys
import time
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 Starting SocraticEd platform...")

    # Backend
    backend_cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app", "--reload", "--port", "8000"
    ]
    backend = subprocess.Popen(backend_cmd, cwd=os.path.join(ROOT, "backend"))

    time.sleep(2)

    # Student
    student = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
        cwd=os.path.join(ROOT, "apps/student")
    )

    # Teacher
    teacher = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8502"],
        cwd=os.path.join(ROOT, "apps/teacher")
    )

    # Parent
    parent = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8503"],
        cwd=os.path.join(ROOT, "apps/parent")
    )

    print("\n✅ All services starting:")
    print("  Backend:   http://localhost:8000/docs")
    print("  Student:   http://localhost:8501")
    print("  Teacher:   http://localhost:8502")
    print("  Parent:    http://localhost:8503")
    print("\nPress Ctrl+C to stop everything.")

    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        for p in [backend, student, teacher, parent]:
            p.terminate()
        print("Done.")

if __name__ == "__main__":
    main()
