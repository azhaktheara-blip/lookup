"""
THEARA COLOR — Projects Endpoints
Founder: Krai Theara | "Create Your Look"
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.core.security import get_current_user
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


class CreateProjectRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


@router.post("")
def create_project(
    payload: CreateProjectRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    return ProjectService.create_project(
        user_id=current_user["id"],
        title=payload.title,
        description=payload.description,
    )


@router.get("")
def list_projects(current_user: Dict[str, Any] = Depends(get_current_user)) -> List[Dict[str, Any]]:
    return ProjectService.list_projects(current_user["id"])

