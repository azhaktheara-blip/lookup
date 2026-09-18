"""
THEARA COLOR — Asset Upload and Management Endpoints
Founder: Krai Theara | "Create Your Look"
"""

import os
from typing import Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from app.core.security import get_current_user
from app.services.project_service import ProjectService
from app.core.config import settings

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.post("/upload")
async def upload_asset(
    file: UploadFile = File(...),
    asset_type: str = Form("original"),  # "original" or "reference"
    project_id: Optional[str] = Form(None),
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    try:
        content = await file.read()
        asset = ProjectService.save_asset(
            user_id=current_user["id"],
            project_id=project_id,
            asset_type=asset_type,
            filename=file.filename or "upload.jpg",
            mime_type=file.content_type or "image/jpeg",
            file_bytes=content,
        )
        asset["url"] = f"/storage/{asset['storage_path'].replace(os.sep, '/')}"
        return asset
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Asset upload failed: {str(e)}")

