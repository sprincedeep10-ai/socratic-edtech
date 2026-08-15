"""Initialize database with HK bilingual models.

Run with: python init_db.py
This drops and recreates tables + seeds realistic HK student data.
"""

from app.database import engine
from app import models
from sqlalchemy.orm import Session
from datetime import datetime

# Recreate all tables
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

print("✅ Tables created with HK bilingual support")

with Session(engine) as db:
    # === HK Students ===
    student1 = models.User(
        id=1,
        name="Alex Chan",
        cantonese_name="陳偉豪",
        role="student",
        email="alex.chan@example.hk",
        language_preference="bilingual",
        school_district="Sham Shui Po"
    )
    
    teacher = models.User(
        id=2,
        name="Ms. Wong Mei Ling",
        cantonese_name="黃美玲",
        role="teacher",
        email="ms.wong@school.hk",
        language_preference="bilingual",
        school_district="Sham Shui Po"
    )
    
    parent = models.User(
        id=3,
        name="Mrs. Chan",
        cantonese_name="陳太",
        role="parent",
        email="parent.chan@example.hk",
        language_preference="bilingual"
    )
    
    db.add_all([student1, teacher, parent])
    db.flush()

    # === Cognitive Error Tags (bilingual for HK) ===
    tag1 = models.CognitiveErrorTag(
        name_en="Fraction Expansion Gaps",
        name_yue="分數擴展缺口",
        category="fractions",
        description_en="Difficulty understanding why numerator and denominator change proportionally when expanding fractions.",
        description_yue="唔明白點解分子同分母擴展時要成比例改變。",
        example_scenario="Student writes 1/2 = 2/4 but cannot explain the 'why' or show equivalent parts."
    )
    
    tag2 = models.CognitiveErrorTag(
        name_en="Procedural vs Conceptual Confusion",
        name_yue="程序與概念混淆",
        category="metacognition",
        description_en="Can follow steps but lacks understanding of the underlying mathematical idea.",
        description_yue="識得跟步驟，但唔明白背後嘅數學概念。",
        example_scenario="Student correctly adds fractions with different denominators using algorithm but cannot draw a diagram."
    )
    
    tag3 = models.CognitiveErrorTag(
        name_en="Prior Knowledge Gap - Multiples",
        name_yue="倍數前備知識缺口",
        category="fractions",
        description_en="Weak foundation in multiples and factors prevents fraction work.",
        description_yue="倍數同因數基礎弱，影響分數學習。",
        example_scenario="Cannot list multiples of 4 or 6 quickly."
    )
    
    db.add_all([tag1, tag2, tag3])
    db.flush()

    # === Learning Gaps ===
    gap1 = models.LearningGap(
        student_id=student1.id,
        tag_id=tag1.id,
        severity=0.82,
        evidence_count=7,
        context_notes="Observed in worksheet Q4-7 and during Socratic chat on 2026-08-14"
    )
    gap2 = models.LearningGap(
        student_id=student1.id,
        tag_id=tag3.id,
        severity=0.65,
        evidence_count=4
    )
    db.add_all([gap1, gap2])

    # === Conversation + Messages (bilingual example) ===
    conv = models.Conversation(
        student_id=student1.id,
        language_used="bilingual"
    )
    db.add(conv)
    db.flush()

    msg1 = models.Message(
        conversation_id=conv.id,
        role="student",
        content="I don't get why 1/2 becomes 2/4 when I multiply top and bottom by 2.",
        language="en"
    )
    msg2 = models.Message(
        conversation_id=conv.id,
        role="assistant",
        content="如果我將1/2嘅餅切成兩半，再將每半再切成兩半，變成四份，你覺得而家1/2等於幾多份？",
        language="yue",
        socratic_strategy="probe_reasoning"
    )
    db.add_all([msg1, msg2])

    # === Teacher Intervention Log ===
    log1 = models.TeacherInterventionLog(
        teacher_id=teacher.id,
        student_id=student1.id,
        tag_id=tag1.id,
        intervention_type="socratic_prompt",
        description_en="Asked student to use pizza diagram to show 1/2 = 2/4",
        description_yue="用薄餅圖解釋1/2等於2/4",
        outcome="partial",
        notes="Student could draw it but still hesitated on verbal explanation. Follow up needed."
    )
    db.add(log1)

    # === Parent Micro-Action Delivery ===
    action1 = models.ParentMicroActionDelivery(
        parent_id=parent.id,
        student_id=student1.id,
        action_text_en="Tonight, ask Alex to explain why multiplying top and bottom by the same number keeps the fraction the same. Use two pieces of paper to cut and show.",
        action_text_yue="今晚問阿豪點解分子同分母同時乘同一數，分數值唔變。用兩張紙剪一剪俾佢睇。",
        status="delivered",
        language_delivered="bilingual",
        delivered_at=datetime.now()
    )
    db.add(action1)

    db.commit()

print("✅ HK bilingual seed data inserted")
print("   - Student: Alex Chan (陳偉豪), Sham Shui Po, bilingual")
print("   - Tags: Fraction Expansion Gaps (分數擴展缺口), etc.")
print("   - Gaps, Interventions, and Parent Actions logged")
print("\nDatabase ready at data/socratic.db")