from __future__ import annotations

from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field

# Import related schemas directly instead of using forward references
from app.schemas.rd_feasibility import RDFeasibility
from app.schemas.rd_customer_interest import RDCustomerInterest
from app.schemas.rd_sample import RDSample
from app.schemas.rd_contact import RDContact
from app.schemas.rd_milestone import RDMilestone
from app.schemas.rd_expense import RDExpense
from app.schemas.rd_revenue import RDRevenue
from app.schemas.rd_note import RDNote
from app.schemas.rd_roi import RDROI


class RDInitiativeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    stage: str = "feasibility"
    target_market: Optional[str] = None
    market_size_estimate: Optional[float] = None
    target_price: Optional[float] = None
    target_margin: Optional[float] = None
    start_date: Optional[date] = None
    target_launch_date: Optional[date] = None
    actual_launch_date: Optional[date] = None
    is_active: str = "active"
    priority: str = "medium"
    lead_owner: Optional[str] = None


class RDInitiativeCreate(RDInitiativeBase):
    pass


class RDInitiativeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[str] = None
    target_market: Optional[str] = None
    market_size_estimate: Optional[float] = None
    target_price: Optional[float] = None
    target_margin: Optional[float] = None
    start_date: Optional[date] = None
    target_launch_date: Optional[date] = None
    actual_launch_date: Optional[date] = None
    is_active: Optional[str] = None
    priority: Optional[str] = None
    lead_owner: Optional[str] = None


class RDInitiative(RDInitiativeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RDInitiativeDetail(RDInitiative):
    """Initiative with all related data"""
    feasibility: Optional[RDFeasibility] = None
    customer_interests: List[RDCustomerInterest] = []
    samples: List[RDSample] = []
    contacts: List[RDContact] = []
    milestones: List[RDMilestone] = []
    expenses: List[RDExpense] = []
    revenue: List[RDRevenue] = []
    notes: List[RDNote] = []
    roi_data: Optional[RDROI] = None
    
    class Config:
        from_attributes = True