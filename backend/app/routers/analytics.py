from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database, schemas
from typing import List

router = APIRouter()

@router.get("/gaps/{student_id}", response_model=List[schemas.LearningGapOut])
def get_gaps(student_id: int, db: Session = Depends(database.get_db)):
    gaps = crud.get_student_gaps(db, student_id)
    return [schemas.LearningGapOut.model_validate(g) for g in gaps]

@router.get("/zero-click-actions/{student_id}")
def get_zero_click_actions(student_id: int, db: Session = Depends(database.get_db)):
    gaps = crud.get_student_gaps(db, student_id)
    actions = []
    for g in gaps:
        if g.severity > 0.6:
            tag = g.tag
            name_en = getattr(tag, 'name_en', None) if tag else None
            name_yue = getattr(tag, 'name_yue', None) if tag else None
            tag_name = name_en or str(g.tag_id)
            tag_display = f"{name_en} ({name_yue})" if name_yue else tag_name
            actions.append({
                "action": f"Assign targeted mini-lesson on {tag_display}",
                "priority": "high",
                "tag": tag_name,
                "tag_en": name_en,
                "tag_yue": name_yue
            })
    if not actions:
        actions.append({"action": "Student is progressing well. Consider enrichment challenge.", "priority": "low"})
    return {"student_id": student_id, "recommended_actions": actions}
