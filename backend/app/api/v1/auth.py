"""
THEARA COLOR — Authentication Endpoints
Founder: Krai Theara | "Create Your Look"
"""

import uuid
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.db.database import get_db
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


class AuthRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=120)
    password: str
    display_name: str = "Creator"


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=120)
    password: str


@router.post("/signup")
def signup(payload: AuthRequest) -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM profiles WHERE email = ?", (payload.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Account with this email already exists")

    user_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO profiles (id, email, display_name, plan_tier) VALUES (?, ?, ?, 'creator')",
        (user_id, payload.email, payload.display_name)
    )
    cursor.execute(
        "INSERT INTO credits (user_id, balance, lifetime_used) VALUES (?, ?, 0)",
        (user_id, settings.PLAN_CREDITS["creator"])
    )
    conn.commit()
    conn.close()

    token = create_access_token({"sub": user_id, "email": payload.email, "display_name": payload.display_name, "plan_tier": "creator"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": payload.email,
            "display_name": payload.display_name,
            "plan_tier": "creator",
            "credits": settings.PLAN_CREDITS["creator"],
        }
    }


@router.post("/login")
def login(payload: LoginRequest) -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE email = ?", (payload.email,))
    user = cursor.fetchone()
    if not user:
        # For prototype/demo convenience, auto-create account on first login
        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO profiles (id, email, display_name, plan_tier) VALUES (?, ?, 'Creator', 'creator')",
            (user_id, payload.email)
        )
        cursor.execute(
            "INSERT INTO credits (user_id, balance, lifetime_used) VALUES (?, ?, 0)",
            (user_id, settings.PLAN_CREDITS["creator"])
        )
        conn.commit()
        cursor.execute("SELECT * FROM profiles WHERE id = ?", (user_id,))
        user = cursor.fetchone()

    user_dict = dict(user)
    conn.close()

    token = create_access_token({
        "sub": user_dict["id"],
        "email": user_dict["email"],
        "display_name": user_dict["display_name"],
        "plan_tier": user_dict["plan_tier"],
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_dict,
    }


@router.get("/me")
def me(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM credits WHERE user_id = ?", (current_user["id"],))
    row = cursor.fetchone()
    conn.close()
    current_user["credits"] = row["balance"] if row else 50
    return current_user
