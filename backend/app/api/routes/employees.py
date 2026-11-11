from fastapi import APIRouter

from app.services.crm_service import list_employees

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("")
def get_employees():
    return list_employees()
