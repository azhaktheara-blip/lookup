"""
THEARA COLOR — Database & Storage Layer (Supabase + Local SQLite Transactional Fallback)
Founder: Krai Theara | "Create Your Look"
"""

import sqlite3
import json
import os
from typing import Dict, Any, List, Optional
from app.core.config import settings

DB_FILE = os.path.join(settings.STORAGE_DIR, "theara_color.db")


def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Profiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        display_name TEXT,
        avatar_url TEXT,
        plan_tier TEXT DEFAULT 'creator',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Credits & Subscriptions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credits (
        user_id TEXT PRIMARY KEY,
        balance INTEGER NOT NULL DEFAULT 50,
        lifetime_used INTEGER NOT NULL DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credit_transactions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        amount INTEGER NOT NULL,
        action TEXT NOT NULL,
        reference_id TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Projects
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Assets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id TEXT PRIMARY KEY,
        project_id TEXT,
        user_id TEXT NOT NULL,
        asset_type TEXT NOT NULL,
        storage_path TEXT NOT NULL,
        filename TEXT NOT NULL,
        mime_type TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        width INTEGER,
        height INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Looks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS looks (
        id TEXT PRIMARY KEY,
        project_id TEXT,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        prompt TEXT,
        parameters TEXT NOT NULL,
        look_dna TEXT NOT NULL,
        original_asset_id TEXT,
        preview_url TEXT,
        is_public INTEGER DEFAULT 0,
        category TEXT DEFAULT 'Cinematic',
        downloads_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Generations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS generations (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        project_id TEXT,
        prompt TEXT NOT NULL,
        reference_asset_id TEXT,
        parameters_generated TEXT,
        look_dna TEXT,
        cost_credits INTEGER NOT NULL DEFAULT 10,
        status TEXT NOT NULL DEFAULT 'completed',
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Exports
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exports (
        id TEXT PRIMARY KEY,
        look_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        format TEXT NOT NULL,
        lut_size INTEGER DEFAULT 33,
        storage_path TEXT NOT NULL,
        download_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert default creator user if not exists
    cursor.execute("SELECT id FROM profiles WHERE id = '00000000-0000-0000-0000-000000000001'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO profiles (id, email, display_name, plan_tier)
        VALUES ('00000000-0000-0000-0000-000000000001', 'creator@thearacolor.io', 'Krai Theara', 'pro')
        """)
        cursor.execute("""
        INSERT INTO credits (user_id, balance, lifetime_used)
        VALUES ('00000000-0000-0000-0000-000000000001', 250, 0)
        """)

    conn.commit()
    conn.close()


init_db()

