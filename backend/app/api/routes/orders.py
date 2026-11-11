from fastapi import APIRouter, HTTPException

from app.services.crm_service import get_order_detail, list_orders

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("")
def get_orders():
    return list_orders()


@router.get("/{order_id}")
def get_order_by_id(order_id: int):
    order = get_order_detail(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
