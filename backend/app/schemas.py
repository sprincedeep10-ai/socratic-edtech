from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Bilingual support
class Language(str):
    pass

class CognitiveErrorTagOut(BaseModel):
    id: int
    name_en: str
    name_yue: str
    category: str
    description_en: Optional[str] = None
    description_yue: Optional[str] = None

class LearningGapOut(BaseModel):
    id: int
    student_id: int
    tag_id: int
    severity: float
    evidence_count: int
    tag: Optional[CognitiveErrorTagOut] = None

class TeacherInterventionLogOut(BaseModel):
    id: int
    teacher_id: int
    student_id: int
    tag_id: Optional[int]
    intervention_type: str
    description_en: Optional[str]
    description_yue: Optional[str]
    outcome: Optional[str]
    timestamp: datetime

class ParentMicroActionDeliveryOut(BaseModel):
    id: int
    parent_id: int
    student_id: int
    action_text_en: str
    action_text_yue: str
    status: str
    language_delivered: str
    delivered_at: Optional[datetime]
    viewed_at: Optional[datetime]
    completed_at: Optional[datetime]

class MessageCreate(BaseModel):
    content: str
    language: str = "en"

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    language: str = "en"
    socratic_strategy: Optional[str] = None
    bottleneck_tags: Optional[list] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    message: MessageOut
    suggested_next_question: Optional[str] = None
    detected_bottlenecks: List[str] = []

# For parent summaries
class ParentSummaryOut(BaseModel):
    summary_text: str
    micro_actions: List[str]
    generated_at: str