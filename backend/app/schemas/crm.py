from pydantic import BaseModel, Field
from typing import Any


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    phone: str | None = None
    city: str | None = None
    state: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class LeadBase(BaseModel):
    lead_name: str = Field(..., min_length=1)
    source: str | None = None
    status: str | None = None
    assigned_to: str | None = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    pass


class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1)
    category: str | None = None
    price: float | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class OrderQuery(BaseModel):
    status: str | None = None


class AIQuery(BaseModel):
    question: str = Field(..., min_length=1)


class APIResponse(BaseModel):
    success: bool = True
    data: Any | None = None
    message: str | None = None
