-- SocraticEd Database Schema
-- Optimized for Hong Kong students (bilingual English / Cantonese)
-- Use with SQLite or PostgreSQL

-- Users (students, teachers, parents)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cantonese_name TEXT,
    role TEXT NOT NULL CHECK(role IN ('student','teacher','parent')),
    email TEXT UNIQUE,
    language_preference TEXT DEFAULT 'bilingual' CHECK(language_preference IN ('en','yue','bilingual')),
    school_district TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Cognitive Error Tags (bilingual)
CREATE TABLE cognitive_error_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_en TEXT NOT NULL,
    name_yue TEXT NOT NULL,
    category TEXT NOT NULL,
    description_en TEXT,
    description_yue TEXT,
    example_scenario TEXT
);

-- Conversations
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES users(id),
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    language_used TEXT DEFAULT 'bilingual'
);

-- Messages (with language tracking)
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER REFERENCES conversations(id),
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    socratic_strategy TEXT,
    bottleneck_tags TEXT,           -- JSON stored as text
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Learning Gaps (linked to proper tags)
CREATE TABLE learning_gaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES users(id),
    tag_id INTEGER REFERENCES cognitive_error_tags(id),
    severity REAL DEFAULT 0.5,
    evidence_count INTEGER DEFAULT 1,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    context_notes TEXT
);

-- Teacher Intervention Logs
CREATE TABLE teacher_intervention_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER REFERENCES users(id),
    student_id INTEGER REFERENCES users(id),
    tag_id INTEGER REFERENCES cognitive_error_tags(id),
    intervention_type TEXT,
    description_en TEXT,
    description_yue TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    outcome TEXT,
    notes TEXT
);

-- Parent Micro-Action Delivery States
CREATE TABLE parent_micro_action_deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER REFERENCES users(id),
    student_id INTEGER REFERENCES users(id),
    action_text_en TEXT,
    action_text_yue TEXT,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending','delivered','viewed','completed','skipped')),
    language_delivered TEXT DEFAULT 'bilingual',
    delivered_at DATETIME,
    viewed_at DATETIME,
    completed_at DATETIME,
    feedback TEXT
);

-- Indexes for common queries
CREATE INDEX idx_gaps_student ON learning_gaps(student_id);
CREATE INDEX idx_interventions_student ON teacher_intervention_logs(student_id);
CREATE INDEX idx_actions_student ON parent_micro_action_deliveries(student_id);
