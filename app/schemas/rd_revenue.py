from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDRevenueBase(BaseModel):
    initiative_id: int
    customer_name: str
    customer_interest_id: Optional[int] = None
    order_number: Optional[str] = None
    order_value: float
    order_date: date
    product_launched: str = "no"  # yes, no
    notes: Optional[str] = None


class RDRevenueCreate(RDRevenueBase):
    pass


class RDRevenueUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_interest_id: Optional[int] = None
    order_number: Optional[str] = None
    order_value: Optional[float] = None
    order_date: Optional[date] = None
    product_launched: Optional[str] = None
    notes: Optional[str] = None


class RDRevenue(RDRevenueBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True