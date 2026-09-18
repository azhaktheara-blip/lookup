"""
THEARA COLOR — Look Generation & Preview Endpoints
Founder: Krai Theara | "Create Your Look"
"""

import os
import uuid
import json
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from PIL import Image
from app.core.security import get_current_user
from app.core.config import settings
from app.services.credit_service import CreditService
from app.services.ai_service import AIStyleInterpreter
from color_engine.models import ColorGradeModel, LookDNA
from color_engine.transforms import process_image
from color_engine.reference import analyze_reference_match
from app.db.database import get_db

router = APIRouter(prefix="/generations", tags=["Generations"])


class GenerateLookRequest(BaseModel):
    prompt: str = Field(..., description="Creator style prompt in natural language")
    original_asset_id: str = Field(..., description="Original image asset ID")
    reference_asset_id: Optional[str] = Field(None, description="Optional visual reference asset ID")
    project_id: Optional[str] = None
    intensity: float = Field(1.0, ge=0.0, le=2.0)


class RenderPreviewRequest(BaseModel):
    original_asset_id: str
    parameters: ColorGradeModel


@router.post("")
async def generate_look(
    payload: GenerateLookRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    user_id = current_user["id"]
    cost = settings.CREDIT_COSTS["reference_match"] if payload.reference_asset_id else settings.CREDIT_COSTS["generation"]

    # 1. Atomic credit deduction
    success, msg = CreditService.deduct_credits(
        user_id=user_id,
        amount=cost,
        action="generation" if not payload.reference_asset_id else "reference_analysis",
        description=f"Generate look: '{payload.prompt[:40]}...'",
    )
    if not success:
        raise HTTPException(status_code=402, detail=msg)

    gen_id = str(uuid.uuid4())

    try:
        # 2. Fetch original image
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assets WHERE id = ?", (payload.original_asset_id,))
        orig_row = cursor.fetchone()
        if not orig_row:
            raise ValueError("Original image asset not found")

        orig_path = os.path.join(settings.STORAGE_DIR, orig_row["storage_path"])
        orig_img = Image.open(orig_path).convert("RGB")

        # 3. AI Style Interpretation or Reference Matching
        if payload.reference_asset_id:
            cursor.execute("SELECT * FROM assets WHERE id = ?", (payload.reference_asset_id,))
            ref_row = cursor.fetchone()
            if not ref_row:
                raise ValueError("Reference image asset not found")
            ref_path = os.path.join(settings.STORAGE_DIR, ref_row["storage_path"])
            ref_img = Image.open(ref_path).convert("RGB")

            # Statistical transfer
            ref_grade, ref_dna = analyze_reference_match(orig_img, ref_img)
            # If user also provided prompt, refine with AI interpreter
            if payload.prompt and len(payload.prompt.strip()) > 3:
                grade, dna = await AIStyleInterpreter.interpret_prompt(payload.prompt, base_grade=ref_grade)
            else:
                grade, dna = ref_grade, ref_dna
        else:
            # Natural language prompt interpretation
            grade, dna = await AIStyleInterpreter.interpret_prompt(payload.prompt)

        grade.intensity = payload.intensity

        # 4. Process image through deterministic Color Engine
        preview_img = process_image(orig_img, grade)

        # 5. Save preview
        preview_filename = f"preview_{gen_id}.webp"
        preview_rel = os.path.join("previews", preview_filename)
        preview_abs = os.path.join(settings.STORAGE_DIR, preview_rel)
        preview_img.save(preview_abs, format="WEBP", quality=92)
        preview_url = f"/storage/{preview_rel.replace(os.sep, '/')}"

        # 6. Record generation in DB
        cursor.execute("""
            INSERT INTO generations (
                id, user_id, project_id, prompt, reference_asset_id,
                parameters_generated, look_dna, cost_credits, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'completed')
        """, (
            gen_id,
            user_id,
            payload.project_id,
            payload.prompt,
            payload.reference_asset_id,
            grade.model_dump_json(),
            dna.model_dump_json(),
            cost,
        ))
        conn.commit()
        conn.close()

        # Fetch updated credits
        balance_info = CreditService.get_balance(user_id)

        return {
            "generation_id": gen_id,
            "preview_url": preview_url,
            "parameters": grade.model_dump(),
            "look_dna": dna.model_dump(),
            "credits_remaining": balance_info["balance"],
        }

    except Exception as e:
        # Automatic refund on failure!
        CreditService.refund_credits(
            user_id=user_id,
            amount=cost,
            reference_id=gen_id,
            reason=f"Failed generation: {str(e)}",
        )
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.post("/render-preview")
async def render_preview(
    payload: RenderPreviewRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Sub-second preview renderer for real-time slider updates (does not consume generation credits).
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assets WHERE id = ?", (payload.original_asset_id,))
    orig_row = cursor.fetchone()
    conn.close()
    if not orig_row:
        raise HTTPException(status_code=404, detail="Original image asset not found")

    orig_path = os.path.join(settings.STORAGE_DIR, orig_row["storage_path"])
    try:
        orig_img = Image.open(orig_path).convert("RGB")
        preview_img = process_image(orig_img, payload.parameters)

        render_id = str(uuid.uuid4())
        preview_filename = f"preview_rt_{render_id}.webp"
        preview_rel = os.path.join("previews", preview_filename)
        preview_abs = os.path.join(settings.STORAGE_DIR, preview_rel)
        preview_img.save(preview_abs, format="WEBP", quality=90)

        return {
            "preview_url": f"/storage/{preview_rel.replace(os.sep, '/')}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview render error: {str(e)}")

