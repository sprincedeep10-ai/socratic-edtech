from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database, schemas
from typing import List

router = APIRouter()

@router.get("/gaps/{student_id}", response_model=List[schemas.LearningGapOut])
def get_gaps(student_id: int, db: Session = Depends(database.get_db)):
    gaps = crud.get_student_gaps(db, student_id)
    return [
        schemas.LearningGapOut(
            bottleneck_tag=g.bottleneck_tag,
            severity=g.severity,
            evidence_count=g.evidence_count
        ) for g in gaps
    ]

@router.get("/zero-click-actions/{student_id}")
def get_zero_click_actions(student_id: int, db: Session = Depends(database.get_db)):
    gaps = crud.get_student_gaps(db, student_id)
    actions = []
    for g in gaps:
        if g.severity > 0.6:
            actions.append({
                "action": f"Assign targeted mini-lesson on {g.bottleneck_tag.replace('_', ' ')}",
                "priority": "high",
                "tag": g.bottleneck_tag
            })
    if not actions:
        actions.append({"action": "Student is progressing well. Consider enrichment challenge.", "priority": "low"})
    return {"student_id": student_id, "recommended_actions": actions}
