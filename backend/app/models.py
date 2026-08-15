from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

# Bilingual language preference for HK students
class LanguagePreference(str, enum.Enum):
    EN = "en"           # English only
    YUE = "yue"         # Cantonese only (Traditional Chinese preferred)
    BILINGUAL = "bilingual"  # English + Cantonese (default for HK)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # English name
    cantonese_name = Column(String, nullable=True)  # 粵語名 e.g. "阿偉"
    role = Column(String, nullable=False)  # student | teacher | parent
    email = Column(String, unique=True, index=True)
    
    # HK localization
    language_preference = Column(String, default=LanguagePreference.BILINGUAL.value)
    school_district = Column(String, nullable=True)  # e.g. "Sham Shui Po", "Kowloon City", "New Territories"

    # Relationships
    conversations = relationship("Conversation", back_populates="student")
    learning_gaps = relationship("LearningGap", back_populates="student")
    interventions = relationship("TeacherInterventionLog", back_populates="student")
    micro_actions = relationship("ParentMicroActionDelivery", back_populates="student")

class CognitiveErrorTag(Base):
    __tablename__ = "cognitive_error_tags"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String, nullable=False)           # "Fraction Expansion Gaps"
    name_yue = Column(String, nullable=False)          # "分數擴展缺口" or Jyutping "fan6 sou3 kwong3 zim2 kyut3 hau2"
    category = Column(String, nullable=False)          # "fractions", "algebra", "geometry", "metacognition"
    description_en = Column(Text)
    description_yue = Column(Text)
    example_scenario = Column(Text)                    # "Student expands 1/2 to 2/4 but cannot explain why denominator changes"

    # Relationships
    learning_gaps = relationship("LearningGap", back_populates="tag")
    interventions = relationship("TeacherInterventionLog", back_populates="tag")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    language_used = Column(String, default="bilingual")  # en | yue | bilingual for this session

    student = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)  # student | assistant
    content = Column(Text)
    language = Column(String, default="en")  # en or yue for this message
    socratic_strategy = Column(String, nullable=True)
    bottleneck_tags = Column(JSON, nullable=True)  # legacy list, prefer LearningGap + tag_id
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")

class LearningGap(Base):
    __tablename__ = "learning_gaps"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    tag_id = Column(Integer, ForeignKey("cognitive_error_tags.id"), nullable=False)
    severity = Column(Float, default=0.5)  # 0.0 - 1.0
    evidence_count = Column(Integer, default=1)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    context_notes = Column(Text, nullable=True)  # e.g. "Observed during fraction worksheet Q3-5"

    student = relationship("User", back_populates="learning_gaps")
    tag = relationship("CognitiveErrorTag", back_populates="learning_gaps")

class TeacherInterventionLog(Base):
    __tablename__ = "teacher_intervention_logs"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    tag_id = Column(Integer, ForeignKey("cognitive_error_tags.id"), nullable=True)
    intervention_type = Column(String)  # "socratic_prompt", "mini_lesson", "peer_discussion", "homework_adjust"
    description_en = Column(Text)
    description_yue = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    outcome = Column(String, nullable=True)  # "improved", "partial", "no_change", "needs_followup"
    notes = Column(Text, nullable=True)

    student = relationship("User", foreign_keys=[student_id], back_populates="interventions")
    tag = relationship("CognitiveErrorTag", back_populates="interventions")

class ParentMicroActionDelivery(Base):
    __tablename__ = "parent_micro_action_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    action_text_en = Column(Text)
    action_text_yue = Column(Text)
    status = Column(String, default="pending")  # pending, delivered, viewed, completed, skipped
    language_delivered = Column(String, default="bilingual")
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    viewed_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    feedback = Column(Text, nullable=True)  # optional parent note

    student = relationship("User", foreign_keys=[student_id], back_populates="micro_actions")
