from fastapi import APIRouter

from app.services.crm_service import get_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def dashboard_overview():
    return get_dashboard_summary()
