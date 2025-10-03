from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    level: int = 1
    total_budget: float = 0.0
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: str = "active"

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None 
    total_budget: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[str] = None

class Campaign(CampaignBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CampaignWithChildren(Campaign):
    children: List[Campaign] = []
    
    class Config:
        from_attributes = True