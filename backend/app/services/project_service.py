"""
THEARA COLOR — Project, Asset, and Look Management Service
Founder: Krai Theara | "Create Your Look"
"""

import uuid
import json
import re
import os
from typing import List, Dict, Any, Optional
from PIL import Image
from app.db.database import get_db
from app.core.config import settings
from color_engine.models import ColorGradeModel, LookDNA


class ProjectService:

    @staticmethod
    def create_project(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        conn = get_db()
        cursor = conn.cursor()
        project_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO projects (id, user_id, title, description) VALUES (?, ?, ?, ?)",
            (project_id, user_id, title, description or "")
        )
        conn.commit()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = dict(cursor.fetchone())
        conn.close()
        return row

    @staticmethod
    def list_projects(user_id: str) -> List[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE user_id = ? ORDER BY updated_at DESC", (user_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def save_asset(
        user_id: str,
        project_id: Optional[str],
        asset_type: str,
        filename: str,
        mime_type: str,
        file_bytes: bytes,
    ) -> Dict[str, Any]:
        # Validate MIME & size (max 25MB)
        if len(file_bytes) > 25 * 1024 * 1024:
            raise ValueError("File exceeds maximum allowed size of 25MB")

        allowed_mimes = ["image/jpeg", "image/png", "image/webp"]
        if mime_type not in allowed_mimes:
            raise ValueError(f"Unsupported file format '{mime_type}'. Please upload JPEG, PNG, or WebP.")

        asset_id = str(uuid.uuid4())
        ext = filename.split(".")[-1].lower() if "." in filename else "jpg"
        save_filename = f"{asset_id}.{ext}"
        storage_rel = os.path.join("uploads", save_filename)
        storage_abs = os.path.join(settings.STORAGE_DIR, storage_rel)

        with open(storage_abs, "wb") as f:
            f.write(file_bytes)

        # Inspect dimensions
        try:
            with Image.open(storage_abs) as img:
                width, height = img.size
        except Exception:
            width, height = None, None

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO assets (id, project_id, user_id, asset_type, storage_path, filename, mime_type, file_size, width, height)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (asset_id, project_id, user_id, asset_type, storage_rel, filename, mime_type, len(file_bytes), width, height))
        conn.commit()
        cursor.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
        row = dict(cursor.fetchone())
        conn.close()
        return row

    @staticmethod
    def save_look(
        user_id: str,
        title: str,
        prompt: str,
        parameters: ColorGradeModel,
        look_dna: LookDNA,
        project_id: Optional[str] = None,
        original_asset_id: Optional[str] = None,
        preview_url: Optional[str] = None,
        is_public: bool = False,
        category: str = "Cinematic",
    ) -> Dict[str, Any]:
        look_id = str(uuid.uuid4())
        # Generate clean URL slug
        base_slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
        slug = f"{base_slug}-{look_id[:6]}"

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO looks (
                id, project_id, user_id, title, slug, prompt,
                parameters, look_dna, original_asset_id, preview_url,
                is_public, category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            look_id,
            project_id,
            user_id,
            title,
            slug,
            prompt,
            parameters.model_dump_json(),
            look_dna.model_dump_json(),
            original_asset_id,
            preview_url,
            1 if is_public else 0,
            category,
        ))
        conn.commit()
        cursor.execute("SELECT * FROM looks WHERE id = ?", (look_id,))
        row = dict(cursor.fetchone())
        conn.close()
        row["parameters"] = json.loads(row["parameters"])
        row["look_dna"] = json.loads(row["look_dna"])
        return row

    @staticmethod
    def list_user_looks(user_id: str) -> List[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM looks WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r["parameters"] = json.loads(r["parameters"])
            r["look_dna"] = json.loads(r["look_dna"])
        return rows

    @staticmethod
    def list_public_looks(category: Optional[str] = None, limit: int = 30) -> List[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.cursor()
        if category and category.lower() != "all":
            cursor.execute(
                "SELECT l.*, p.display_name as creator_name FROM looks l LEFT JOIN profiles p ON l.user_id = p.id WHERE l.is_public = 1 AND LOWER(l.category) = LOWER(?) ORDER BY l.downloads_count DESC, l.created_at DESC LIMIT ?",
                (category, limit)
            )
        else:
            cursor.execute(
                "SELECT l.*, p.display_name as creator_name FROM looks l LEFT JOIN profiles p ON l.user_id = p.id WHERE l.is_public = 1 ORDER BY l.downloads_count DESC, l.created_at DESC LIMIT ?",
                (limit,)
            )
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        for r in rows:
            r["parameters"] = json.loads(r["parameters"])
            r["look_dna"] = json.loads(r["look_dna"])
        return rows

    @staticmethod
    def get_look_by_slug(slug: str) -> Optional[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT l.*, p.display_name as creator_name FROM looks l LEFT JOIN profiles p ON l.user_id = p.id WHERE l.slug = ?",
            (slug,)
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        d = dict(row)
        d["parameters"] = json.loads(d["parameters"])
        d["look_dna"] = json.loads(d["look_dna"])
        return d

