from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDCustomerInterestBase(BaseModel):
    initiative_id: int
    customer_name: str
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    
    # NEW: Strategic intel
    current_product_used: Optional[str] = None
    testing_method: Optional[str] = None
    interest_timeline: Optional[str] = None  # immediate, 30_days, 90_days, future
    
    interest_level: str = "interested"  # interested, highly_interested, committed, testing, ordered, not_interested
    has_order_history: Optional[str] = None  # yes, no
    historical_order_volume: Optional[float] = None
    similar_products_ordered: Optional[str] = None
    first_contact_date: Optional[date] = None
    last_contact_date: Optional[date] = None
    next_follow_up_date: Optional[date] = None
    sample_requested: str = "no"  # yes, no, sent
    sample_sent_date: Optional[date] = None
    notes: Optional[str] = None


class RDCustomerInterestCreate(RDCustomerInterestBase):
    pass


class RDCustomerInterestUpdate(BaseModel):
    customer_name: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    current_product_used: Optional[str] = None
    testing_method: Optional[str] = None
    interest_timeline: Optional[str] = None
    interest_level: Optional[str] = None
    has_order_history: Optional[str] = None
    historical_order_volume: Optional[float] = None
    similar_products_ordered: Optional[str] = None
    first_contact_date: Optional[date] = None
    last_contact_date: Optional[date] = None
    next_follow_up_date: Optional[date] = None
    sample_requested: Optional[str] = None
    sample_sent_date: Optional[date] = None
    notes: Optional[str] = None


class RDCustomerInterest(RDCustomerInterestBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True