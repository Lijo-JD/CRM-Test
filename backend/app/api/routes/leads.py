from fastapi import APIRouter, HTTPException

from app.schemas.crm import LeadCreate, LeadUpdate
from app.services.crm_service import create_lead, delete_lead, list_leads, update_lead

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("")
def get_leads():
    return list_leads()


@router.post("")
def create_new_lead(payload: LeadCreate):
    return create_lead(payload)


@router.put("/{lead_id}")
def update_existing_lead(lead_id: int, payload: LeadUpdate):
    if not any(item["lead_id"] == lead_id for item in list_leads()):
        raise HTTPException(status_code=404, detail="Lead not found")
    return update_lead(lead_id, payload)


@router.delete("/{lead_id}")
def delete_existing_lead(lead_id: int):
    if not any(item["lead_id"] == lead_id for item in list_leads()):
        raise HTTPException(status_code=404, detail="Lead not found")
    return delete_lead(lead_id)
