"""
THEARA COLOR — Credits Endpoints
Founder: Krai Theara | "Create Your Look"
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.services.credit_service import CreditService

router = APIRouter(prefix="/credits", tags=["Credits"])


@router.get("/balance")
def get_balance(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    return CreditService.get_balance(current_user["id"])


@router.get("/transactions")
def get_transactions(current_user: Dict[str, Any] = Depends(get_current_user)) -> List[Dict[str, Any]]:
    return CreditService.get_transactions(current_user["id"])

