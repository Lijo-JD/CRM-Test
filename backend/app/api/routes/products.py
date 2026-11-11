from fastapi import APIRouter, HTTPException

from app.schemas.crm import ProductCreate, ProductUpdate
from app.services.crm_service import create_product, delete_product, list_products, update_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def get_products():
    return list_products()


@router.post("")
def create_new_product(payload: ProductCreate):
    return create_product(payload)


@router.put("/{product_id}")
def update_existing_product(product_id: int, payload: ProductUpdate):
    if not any(item["product_id"] == product_id for item in list_products()):
        raise HTTPException(status_code=404, detail="Product not found")
    return update_product(product_id, payload)


@router.delete("/{product_id}")
def delete_existing_product(product_id: int):
    if not any(item["product_id"] == product_id for item in list_products()):
        raise HTTPException(status_code=404, detail="Product not found")
    return delete_product(product_id)
