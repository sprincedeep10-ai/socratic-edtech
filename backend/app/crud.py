from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
import random

# Simple Socratic + bottleneck simulator (replace with real LLM later)
BOTTLENECK_LIBRARY = [
    "conceptual_misunderstanding",
    "procedural_gap",
    "prior_knowledge_gap",
    "attention_fragmentation",
    "overgeneralization",
    "weak_metacognition"
]

def get_or_create_student(db: Session, name: str = "Alex Rivera"):
    student = db.query(models.User).filter_by(name=name, role="student").first()
    if not student:
        student = models.User(name=name, role="student", email="alex@example.com")
        db.add(student)
        db.commit()
        db.refresh(student)
    return student

def create_message(db: Session, conversation_id: int, role: str, content: str,
                   socratic_strategy: Optional[str] = None,
                   bottleneck_tags: Optional[List[str]] = None):
    msg = models.Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        socratic_strategy=socratic_strategy,
        bottleneck_tags=bottleneck_tags or []
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_or_create_conversation(db: Session, student_id: int):
    conv = db.query(models.Conversation).filter_by(student_id=student_id).first()
    if not conv:
        conv = models.Conversation(student_id=student_id)
        db.add(conv)
        db.commit()
        db.refresh(conv)
    return conv

def detect_bottlenecks(text: str) -> List[str]:
    """Very naive heuristic — replace with LLM classifier later."""
    text = text.lower()
    tags = []
    if any(x in text for x in ["why", "because", "explain"]):
        tags.append("weak_metacognition")
    if any(x in text for x in ["don't understand", "confused", "what does"]):
        tags.append("conceptual_misunderstanding")
    if any(x in text for x in ["how do i", "step", "solve"]):
        tags.append("procedural_gap")
    if not tags:
        tags = random.sample(BOTTLENECK_LIBRARY, k=random.randint(1, 2))
    return list(set(tags))

def generate_socratic_response(student_msg: str, previous_tags: List[str]) -> dict:
    """Prototype Socratic reply generator."""
    tags = detect_bottlenecks(student_msg)
    strategy = "clarify_assumption" if "conceptual_misunderstanding" in tags else "probe_reasoning"

    reply = f"That's interesting. What makes you think that? Can you give me an example of when that happens?"

    if "procedural_gap" in tags:
        reply = "Walk me through the first step you would take. What do you think comes next?"

    return {
        "content": reply,
        "socratic_strategy": strategy,
        "bottleneck_tags": tags
    }

def update_learning_gaps(db: Session, student_id: int, tags: List[str]):
    for tag in tags:
        gap = db.query(models.LearningGap).filter_by(student_id=student_id, bottleneck_tag=tag).first()
        if gap:
            gap.evidence_count += 1
            gap.severity = min(1.0, gap.severity + 0.1)
        else:
            gap = models.LearningGap(student_id=student_id, bottleneck_tag=tag, severity=0.6, evidence_count=1)
            db.add(gap)
    db.commit()

def get_student_gaps(db: Session, student_id: int):
    return db.query(models.LearningGap).filter_by(student_id=student_id).all()
