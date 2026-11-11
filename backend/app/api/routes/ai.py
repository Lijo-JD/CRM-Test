from fastapi import APIRouter

from app.schemas.crm import AIQuery
from app.services.ai_service import ask_crm_secure

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/query")
def query_crm(payload: AIQuery):
    return ask_crm_secure(payload.question)
