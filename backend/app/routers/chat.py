from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter()

@router.post("/message", response_model=schemas.ChatResponse)
def send_student_message(payload: schemas.MessageCreate, db: Session = Depends(database.get_db)):
    student = crud.get_or_create_student(db)
    conv = crud.get_or_create_conversation(db, student.id)

    # Save student message
    student_msg = crud.create_message(
        db, conv.id, role="student", content=payload.content
    )

    # Generate Socratic reply + tags
    ai_response = crud.generate_socratic_response(payload.content, [])
    crud.update_learning_gaps(db, student.id, ai_response["bottleneck_tags"])

    # Save assistant message
    assistant_msg = crud.create_message(
        db,
        conv.id,
        role="assistant",
        content=ai_response["content"],
        socratic_strategy=ai_response["socratic_strategy"],
        bottleneck_tags=ai_response["bottleneck_tags"]
    )

    return schemas.ChatResponse(
        message=schemas.MessageOut.from_orm(assistant_msg),
        suggested_next_question="What do you think would happen if we changed X?",
        detected_bottlenecks=ai_response["bottleneck_tags"]
    )

@router.get("/history/{student_id}", response_model=list[schemas.MessageOut])
def get_chat_history(student_id: int, db: Session = Depends(database.get_db)):
    conv = crud.get_or_create_conversation(db, student_id)
    return [schemas.MessageOut.from_orm(m) for m in conv.messages]
