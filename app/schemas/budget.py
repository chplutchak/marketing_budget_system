from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class BudgetItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str  # e.g., "Digital Ads", "Personnel", "Events"
    total_budget: float = 0.0
    monthly_budget: Optional[Dict[str, float]] = None  # {"1": 1000, "2": 1500, ...}

class BudgetItemCreate(BudgetItemBase):
    campaign_id: int
    cost_center_id: int

class BudgetItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    total_budget: Optional[float] = None
    monthly_budget: Optional[Dict[str, float]] = None

class BudgetItem(BudgetItemBase):
    id: int
    campaign_id: int
    cost_center_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class BudgetItemWithRelations(BudgetItem):
    campaign_name: Optional[str] = None
    cost_center_name: Optional[str] = None
    
    class Config:
        from_attributes = True