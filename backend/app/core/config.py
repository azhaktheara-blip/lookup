"""
THEARA COLOR — Backend Configuration
Founder: Krai Theara | "Create Your Look"
"""

import os
from typing import Dict, Any
from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "THEARA COLOR"
    PRODUCT_TAGLINE: str = "Create Your Look."
    FOUNDER: str = "Krai Theara"
    VERSION: str = "1.0.0"

    # Host & Ports
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "theara-color-super-secure-production-secret-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Supabase / DB
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres.tgqvtmrbwefuouegtsbw:Theara%40%40%4090@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
    )
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # Storage paths
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage")))

    # AI Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "auto")  # auto, gemini, openai, semantic_engine

    # Pricing & Credit Economics
    CREDIT_COSTS: Dict[str, int] = {
        "generation": 10,
        "regenerate": 5,
        "reference_match": 15,
        "export_cube": 0,    # Free once generated
        "export_xmp": 0,
    }

    PLAN_CREDITS: Dict[str, int] = {
        "free": 50,
        "creator": 500,
        "pro": 2000,
        "studio": 10000,
    }

    PRICING_USD: Dict[str, float] = {
        "free": 0.0,
        "creator": 19.0,
        "pro": 49.0,
        "studio": 149.0,
    }


settings = Settings()

# Ensure local storage directory exists
os.makedirs(os.path.join(settings.STORAGE_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_DIR, "previews"), exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_DIR, "exports"), exist_ok=True)

