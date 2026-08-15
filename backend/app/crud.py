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

def get_or_create_student(db: Session, name: str = "Alex Chan"):
    student = db.query(models.User).filter_by(name=name, role="student").first()
    if not student:
        student = models.User(
            name=name, 
            cantonese_name="陳偉豪",
            role="student", 
            email="alex@example.com",
            school_district="Sham Shui Po",
            language_preference="bilingual"
        )
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

    reply = "That's interesting. What makes you think that? Can you give me an example of when that happens?"

    if "procedural_gap" in tags:
        reply = "Walk me through the first step you would take. What do you think comes next?"

    return {
        "content": reply,
        "socratic_strategy": strategy,
        "bottleneck_tags": tags
    }

def update_learning_gaps(db: Session, student_id: int, tags: List[str]):
    # Find or create a default tag for each (simplified for prototype)
    for tag_name in tags:
        tag = db.query(models.CognitiveErrorTag).filter_by(name_en=tag_name).first()
        if not tag:
            tag = models.CognitiveErrorTag(
                name_en=tag_name,
                name_yue=tag_name,
                category="general"
            )
            db.add(tag)
            db.commit()
            db.refresh(tag)

        gap = db.query(models.LearningGap).filter_by(student_id=student_id, tag_id=tag.id).first()
        if gap:
            gap.evidence_count += 1
            gap.severity = min(1.0, gap.severity + 0.1)
        else:
            gap = models.LearningGap(
                student_id=student_id, 
                tag_id=tag.id, 
                severity=0.6, 
                evidence_count=1
            )
            db.add(gap)
    db.commit()

def get_student_gaps(db: Session, student_id: int):
    return db.query(models.LearningGap).filter_by(student_id=student_id).all()
