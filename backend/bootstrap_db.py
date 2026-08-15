#!/usr/bin/env python3
"""
Stdlib-only bootstrap for HK bilingual SocraticEd database.
No SQLAlchemy needed.

Usage:
    cd backend
    python3 bootstrap_db.py
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "socratic.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Clean slate
for table in ["parent_micro_action_deliveries", "teacher_intervention_logs", 
              "learning_gaps", "messages", "conversations", 
              "cognitive_error_tags", "users"]:
    c.execute(f"DROP TABLE IF EXISTS {table}")

# Create tables
c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cantonese_name TEXT,
    role TEXT NOT NULL,
    email TEXT UNIQUE,
    language_preference TEXT DEFAULT 'bilingual',
    school_district TEXT
)
""")

c.execute("""
CREATE TABLE cognitive_error_tags (
    id INTEGER PRIMARY KEY,
    name_en TEXT NOT NULL,
    name_yue TEXT NOT NULL,
    category TEXT NOT NULL,
    description_en TEXT,
    description_yue TEXT,
    example_scenario TEXT
)
""")

c.execute("""
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    student_id INTEGER REFERENCES users(id),
    started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    language_used TEXT DEFAULT 'bilingual'
)
""")

c.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    role TEXT,
    content TEXT,
    language TEXT DEFAULT 'en',
    socratic_strategy TEXT,
    bottleneck_tags TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

c.execute("""
CREATE TABLE learning_gaps (
    id INTEGER PRIMARY KEY,
    student_id INTEGER REFERENCES users(id),
    tag_id INTEGER REFERENCES cognitive_error_tags(id),
    severity REAL DEFAULT 0.5,
    evidence_count INTEGER DEFAULT 1,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    context_notes TEXT
)
""")

c.execute("""
CREATE TABLE teacher_intervention_logs (
    id INTEGER PRIMARY KEY,
    teacher_id INTEGER REFERENCES users(id),
    student_id INTEGER REFERENCES users(id),
    tag_id INTEGER REFERENCES cognitive_error_tags(id),
    intervention_type TEXT,
    description_en TEXT,
    description_yue TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    outcome TEXT,
    notes TEXT
)
""")

c.execute("""
CREATE TABLE parent_micro_action_deliveries (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER REFERENCES users(id),
    student_id INTEGER REFERENCES users(id),
    action_text_en TEXT,
    action_text_yue TEXT,
    status TEXT DEFAULT 'pending',
    language_delivered TEXT DEFAULT 'bilingual',
    delivered_at TEXT,
    viewed_at TEXT,
    completed_at TEXT,
    feedback TEXT
)
""")

# === Seed Hong Kong bilingual data ===

# Users
c.execute("INSERT INTO users (id, name, cantonese_name, role, email, language_preference, school_district) VALUES (1, 'Alex Chan', '陳偉豪', 'student', 'alex.chan@example.hk', 'bilingual', 'Sham Shui Po')")
c.execute("INSERT INTO users (id, name, cantonese_name, role, email, language_preference) VALUES (2, 'Ms. Wong Mei Ling', '黃美玲', 'teacher', 'ms.wong@school.hk', 'bilingual')")
c.execute("INSERT INTO users (id, name, cantonese_name, role, email, language_preference) VALUES (3, 'Mrs. Chan', '陳太', 'parent', 'parent.chan@example.hk', 'bilingual')")

# Cognitive Error Tags (bilingual)
c.execute("""INSERT INTO cognitive_error_tags (id, name_en, name_yue, category, description_en, description_yue, example_scenario)
VALUES (1, 'Fraction Expansion Gaps', '分數擴展缺口', 'fractions',
'Difficulty understanding why numerator and denominator change proportionally when expanding fractions.',
'唔明白點解分子同分母擴展時要成比例改變。',
'Student writes 1/2 = 2/4 but cannot explain why or show with diagram.')""")

c.execute("""INSERT INTO cognitive_error_tags (id, name_en, name_yue, category, description_en, description_yue, example_scenario)
VALUES (2, 'Procedural vs Conceptual Confusion', '程序與概念混淆', 'metacognition',
'Can follow steps but lacks understanding of the idea.',
'識得跟步驟，但唔明白背後概念。',
'Correctly adds fractions but cannot explain with a picture.')""")

c.execute("""INSERT INTO cognitive_error_tags (id, name_en, name_yue, category, description_en, description_yue, example_scenario)
VALUES (3, 'Prior Knowledge Gap - Multiples', '倍數前備知識缺口', 'fractions',
'Weak foundation in multiples and factors blocks fraction work.',
'倍數同因數基礎弱，影響分數學習。',
'Cannot quickly list multiples of 4 or 6.')""")

# Learning Gaps
c.execute("INSERT INTO learning_gaps (student_id, tag_id, severity, evidence_count, context_notes) VALUES (1, 1, 0.82, 7, 'Seen in chat and worksheet Q4-7')")
c.execute("INSERT INTO learning_gaps (student_id, tag_id, severity, evidence_count) VALUES (1, 3, 0.65, 4)")

# Conversation + Messages (bilingual example)
c.execute("INSERT INTO conversations (id, student_id, language_used) VALUES (1, 1, 'bilingual')")
c.execute("INSERT INTO messages (conversation_id, role, content, language) VALUES (1, 'student', 'I don''t get why 1/2 becomes 2/4 when I multiply top and bottom by 2.', 'en')")
c.execute("INSERT INTO messages (conversation_id, role, content, language, socratic_strategy) VALUES (1, 'assistant', '如果我將1/2嘅餅切成兩半，再將每半再切成兩半，變成四份，你覺得而家1/2等於幾多份？', 'yue', 'probe_reasoning')")

# Teacher Intervention Log
c.execute("""INSERT INTO teacher_intervention_logs (teacher_id, student_id, tag_id, intervention_type, description_en, description_yue, outcome, notes)
VALUES (2, 1, 1, 'socratic_prompt',
'Used pizza diagram to show 1/2 = 2/4',
'用薄餅圖解釋1/2等於2/4',
'partial',
'Student could draw but hesitated on verbal explanation.')""")

# Parent Micro-Action Delivery (parameterized to avoid quote hell)
now = datetime.now().isoformat()
c.execute("""INSERT INTO parent_micro_action_deliveries 
(parent_id, student_id, action_text_en, action_text_yue, status, language_delivered, delivered_at)
VALUES (3, 1, ?, ?, 'delivered', 'bilingual', ?)""",
('Tonight ask Alex to explain why multiplying top and bottom by the same number keeps the fraction the same. Use paper cutting to show.',
 '今晚問阿豪點解分子同分母乘同一數，分數值唔變。用紙剪一剪俾佢睇。',
 now))

conn.commit()
conn.close()

print("✅ Database created with Hong Kong bilingual models")
print(f"📁 {os.path.abspath(DB_PATH)}")
print("Tables: users, cognitive_error_tags, learning_gaps, conversations, messages, teacher_intervention_logs, parent_micro_action_deliveries")
print("\nSeed data includes:")
print("  - Student: Alex Chan (陳偉豪) from Sham Shui Po, bilingual preference")
print("  - Tags with English + Cantonese (分數擴展缺口 etc.)")
print("  - Learning gaps, bilingual messages, teacher log, parent action")
