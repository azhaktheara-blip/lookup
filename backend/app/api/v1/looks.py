"""
THEARA COLOR — Looks & Export Endpoints
Founder: Krai Theara | "Create Your Look"
"""

import os
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from app.core.security import get_current_user
from app.services.project_service import ProjectService
from app.services.export_service import ExportService
from color_engine.models import ColorGradeModel, LookDNA

router = APIRouter(prefix="/looks", tags=["Looks"])


class SaveLookRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    prompt: Optional[str] = None
    parameters: ColorGradeModel
    look_dna: LookDNA
    project_id: Optional[str] = None
    original_asset_id: Optional[str] = None
    preview_url: Optional[str] = None
    is_public: bool = False
    category: str = "Cinematic"


class ExportRequest(BaseModel):
    format: str = "cube"  # "cube" or "xmp"
    lut_size: int = 33


@router.post("")
def save_look(
    payload: SaveLookRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    return ProjectService.save_look(
        user_id=current_user["id"],
        title=payload.title,
        prompt=payload.prompt or "",
        parameters=payload.parameters,
        look_dna=payload.look_dna,
        project_id=payload.project_id,
        original_asset_id=payload.original_asset_id,
        preview_url=payload.preview_url,
        is_public=payload.is_public,
        category=payload.category,
    )


@router.get("")
def list_my_looks(current_user: Dict[str, Any] = Depends(get_current_user)) -> List[Dict[str, Any]]:
    return ProjectService.list_user_looks(current_user["id"])


@router.get("/public")
def list_public_looks(category: Optional[str] = Query(None), limit: int = 30) -> List[Dict[str, Any]]:
    return ProjectService.list_public_looks(category=category, limit=limit)


@router.get("/slug/{slug}")
def get_look_by_slug(slug: str) -> Dict[str, Any]:
    look = ProjectService.get_look_by_slug(slug)
    if not look:
        raise HTTPException(status_code=404, detail="Look not found")
    return look


@router.post("/{look_id}/export")
def export_look(
    look_id: str,
    payload: ExportRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    # Retrieve look
    looks = ProjectService.list_user_looks(current_user["id"])
    target_look = next((l for l in looks if l["id"] == look_id), None)
    if not target_look:
        # Also check public looks
        all_public = ProjectService.list_public_looks()
        target_look = next((l for l in all_public if l["id"] == look_id), None)

    if not target_look:
        raise HTTPException(status_code=404, detail="Look not found")

    grade = ColorGradeModel(**target_look["parameters"])
    export_id, abs_path, filename = ExportService.export_look(
        user_id=current_user["id"],
        look_id=look_id,
        export_format=payload.format,
        grade=grade,
        look_title=target_look["title"],
        lut_size=payload.lut_size,
    )

    return FileResponse(
        path=abs_path,
        filename=filename,
        media_type="application/octet-stream",
    )

