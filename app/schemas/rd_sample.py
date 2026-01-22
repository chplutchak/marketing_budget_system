from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDSampleBase(BaseModel):
    initiative_id: int
    sample_type: str  # trial_batch, demo_sample, validation_sample
    recipient_name: str
    recipient_company: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    ship_date: Optional[date] = None
    tracking_number: Optional[str] = None
    sample_cost: float = 0.0
    shipping_cost: Optional[float] = None
    follow_up_date: Optional[date] = None
    feedback_received: str = "no"  # yes, no, pending
    feedback_notes: Optional[str] = None
    converted_to_order: str = "pending"  # yes, no, pending
    order_value: Optional[float] = None
    order_date: Optional[date] = None
    notes: Optional[str] = None


class RDSampleCreate(RDSampleBase):
    pass


class RDSampleUpdate(BaseModel):
    sample_type: Optional[str] = None
    recipient_name: Optional[str] = None
    recipient_company: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    ship_date: Optional[date] = None
    tracking_number: Optional[str] = None
    sample_cost: Optional[float] = None
    shipping_cost: Optional[float] = None
    follow_up_date: Optional[date] = None
    feedback_received: Optional[str] = None
    feedback_notes: Optional[str] = None
    converted_to_order: Optional[str] = None
    order_value: Optional[float] = None
    order_date: Optional[date] = None
    notes: Optional[str] = None


class RDSample(RDSampleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True