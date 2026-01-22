from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDROIBase(BaseModel):
    initiative_id: int
    total_development_cost: float = 0.0
    total_sample_cost: float = 0.0
    total_marketing_cost: float = 0.0
    total_other_costs: float = 0.0
    total_revenue: float = 0.0
    total_orders: int = 0
    total_investment: float = 0.0
    roi_percentage: Optional[float] = None
    samples_sent_count: int = 0
    samples_converted_count: int = 0
    conversion_rate: Optional[float] = None
    notes: Optional[str] = None
    last_calculated_date: Optional[date] = None


class RDROICreate(RDROIBase):
    pass


class RDROIUpdate(BaseModel):
    total_development_cost: Optional[float] = None
    total_sample_cost: Optional[float] = None
    total_marketing_cost: Optional[float] = None
    total_other_costs: Optional[float] = None
    total_revenue: Optional[float] = None
    total_orders: Optional[int] = None
    total_investment: Optional[float] = None
    roi_percentage: Optional[float] = None
    samples_sent_count: Optional[int] = None
    samples_converted_count: Optional[int] = None
    conversion_rate: Optional[float] = None
    notes: Optional[str] = None
    last_calculated_date: Optional[date] = None


class RDROI(RDROIBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True