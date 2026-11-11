from fastapi import APIRouter, HTTPException

from app.schemas.crm import CustomerCreate, CustomerUpdate
from app.services.crm_service import create_customer, delete_customer, get_customer, list_customers, update_customer

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("")
def get_customers():
    return list_customers()


@router.get("/{customer_id}")
def get_customer_by_id(customer_id: int):
    customer = get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("")
def create_new_customer(payload: CustomerCreate):
    return create_customer(payload)


@router.put("/{customer_id}")
def update_existing_customer(customer_id: int, payload: CustomerUpdate):
    if not get_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return update_customer(customer_id, payload)


@router.delete("/{customer_id}")
def delete_existing_customer(customer_id: int):
    if not get_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return delete_customer(customer_id)
