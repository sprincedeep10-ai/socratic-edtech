from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database, models
from ..schemas import ParentSummaryOut
from typing import List

router = APIRouter()

@router.get("/summary/{student_id}", response_model=ParentSummaryOut)
def get_parent_summary(student_id: int, db: Session = Depends(database.get_db)):
    # In real version this would call an LLM
    gaps = crud.get_student_gaps(db, student_id)
    if not gaps:
        return ParentSummaryOut(
            summary_text="Your child is making steady progress. No major concerns right now.",
            micro_actions=["Celebrate their effort this week with a small reward."],
            generated_at="2026-08-15T12:00:00"
        )

    top_gap = max(gaps, key=lambda g: g.severity)
    summary = f"Your child is showing signs of {top_gap.bottleneck_tag.replace('_', ' ')}. " \
              "They may benefit from more 'why' questions during homework."

    micro_actions = [
        f"Ask them to explain one concept in their own words tonight.",
        "Try a 5-minute 'teach me' game on the topic."
    ]

    return ParentSummaryOut(
        summary_text=summary,
        micro_actions=micro_actions,
        generated_at="2026-08-15T12:00:00"
    )
