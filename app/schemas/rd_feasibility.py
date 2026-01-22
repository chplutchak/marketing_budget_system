from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDFeasibilityBase(BaseModel):
    initiative_id: int
    is_manufacturable: Optional[str] = None  # yes, no, needs_research
    manufacturing_complexity: Optional[str] = None  # low, medium, high
    estimated_lead_time_days: Optional[int] = None
    moq: Optional[int] = None
    estimated_cogs: Optional[float] = None
    estimated_development_cost: Optional[float] = None
    estimated_sample_cost: Optional[float] = None
    material_constraints: Optional[str] = None
    supplier_identified: Optional[str] = None  # yes, no, partial
    regulatory_requirements: Optional[str] = None
    regulatory_status: Optional[str] = None
    feasibility_notes: Optional[str] = None
    last_reviewed_date: Optional[date] = None


class RDFeasibilityCreate(RDFeasibilityBase):
    pass


class RDFeasibilityUpdate(BaseModel):
    is_manufacturable: Optional[str] = None
    manufacturing_complexity: Optional[str] = None
    estimated_lead_time_days: Optional[int] = None
    moq: Optional[int] = None
    estimated_cogs: Optional[float] = None
    estimated_development_cost: Optional[float] = None
    estimated_sample_cost: Optional[float] = None
    material_constraints: Optional[str] = None
    supplier_identified: Optional[str] = None
    regulatory_requirements: Optional[str] = None
    regulatory_status: Optional[str] = None
    feasibility_notes: Optional[str] = None
    last_reviewed_date: Optional[date] = None


class RDFeasibility(RDFeasibilityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True