from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Base schema with common fields
class RDProjectBase(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=200)
    product_category: Optional[str] = None
    status: str = "Feasibility"  # Feasibility, Development, Testing, Launch, Active, Discontinued
    priority: str = "Medium"  # High, Medium, Low
    market_opportunity: Optional[str] = None
    competitive_landscape: Optional[str] = None
    target_price_point: Optional[float] = None
    target_margin: Optional[float] = None
    go_no_go_criteria: Optional[str] = None
    launch_target_date: Optional[date] = None


# Schema for creating new R&D project
class RDProjectCreate(RDProjectBase):
    created_by: str


# Schema for updating R&D project
class RDProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    product_category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    market_opportunity: Optional[str] = None
    competitive_landscape: Optional[str] = None
    target_price_point: Optional[float] = None
    target_margin: Optional[float] = None
    go_no_go_criteria: Optional[str] = None
    launch_target_date: Optional[date] = None
    updated_by: Optional[str] = None


# Schema for reading R&D project (includes ID and timestamps)
class RDProject(RDProjectBase):
    id: int
    created_date: date
    created_by: str
    last_updated: Optional[date] = None
    updated_by: Optional[str] = None
    
    class Config:
        from_attributes = True


# Schema with related data (manufacturing, customers, etc.)
class RDProjectDetail(RDProject):
    manufacturing: Optional['RDManufacturing'] = None
    customer_interests: List['RDCustomerInterest'] = []
    samples: List['RDSample'] = []
    expenses: List['RDExpense'] = []
    revenue: List['RDRevenue'] = []
    milestones: List['RDMilestone'] = []
    notes: List['RDNote'] = []
    
    class Config:
        from_attributes = True