from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from .routers import chat, analytics, summaries

app = FastAPI(title="SocraticEd API", version="0.1.0")

models.Base.metadata.create_all(bind=database.engine)

app.include_router(chat.router, prefix="/chat", tags=["Student Chat"])
app.include_router(analytics.router, prefix="/analytics", tags=["Teacher"])
app.include_router(summaries.router, prefix="/parent", tags=["Parent"])

@app.get("/")
def root():
    return {"message": "SocraticEd API is running. See /docs for endpoints."}

@app.get("/health")
def health():
    return {"status": "ok"}
