from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database
from ..schemas import ParentSummaryOut
from typing import List

router = APIRouter()

@router.get("/summary/{student_id}", response_model=ParentSummaryOut)
def get_parent_summary(student_id: int, db: Session = Depends(database.get_db)):
    gaps = crud.get_student_gaps(db, student_id)
    micro_actions_db = crud.get_parent_micro_actions(db, student_id)

    if micro_actions_db:
        # Use the seeded bilingual action(s)
        action = micro_actions_db[0]
        summary_text = "Your child is showing signs of difficulty connecting ideas in math. They understand the steps but struggle with the 'why'."
        micro_actions = [
            f"[EN] {action.action_text_en}",
            f"[粵語] {action.action_text_yue}"
        ]
    elif not gaps:
        return ParentSummaryOut(
            summary_text="Your child is making steady progress. No major concerns right now.",
            micro_actions=["[EN] Celebrate their effort this week with a small reward.", "[粵語] 呢個星期表揚下佢嘅努力，俾少少獎勵。"],
            generated_at="2026-08-16T12:00:00"
        )
    else:
        top_gap = max(gaps, key=lambda g: g.severity)
        tag = top_gap.tag
        name_en = getattr(tag, 'name_en', 'learning gap') if tag else 'learning gap'
        name_yue = getattr(tag, 'name_yue', '') if tag else ''
        tag_display = f"{name_en} ({name_yue})" if name_yue else name_en

        summary_text = f"Your child is showing signs of {name_en}. They may benefit from more 'why' questions during homework."

        micro_actions = [
            f"[EN] Ask them to explain one concept in their own words tonight.",
            f"[粵語] 今晚叫佢用自己嘅話解釋一個概念。"
        ]

    return ParentSummaryOut(
        summary_text=summary_text,
        micro_actions=micro_actions,
        generated_at="2026-08-16T12:00:00"
    )
