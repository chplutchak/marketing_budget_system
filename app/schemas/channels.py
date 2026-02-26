from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MarketingChannelBase(BaseModel):
    year: int
    channel_name: str
    icon: Optional[str] = None
    color: Optional[str] = None
    frequency: str
    days: str
    time_commitment: str
    budget: str
    tactics: Optional[List[str]] = None
    order_position: int = 0

class MarketingChannelCreate(MarketingChannelBase):
    pass

class MarketingChannelUpdate(BaseModel):
    channel_name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    frequency: Optional[str] = None
    days: Optional[str] = None
    time_commitment: Optional[str] = None
    budget: Optional[str] = None
    tactics: Optional[List[str]] = None
    order_position: Optional[int] = None

class MarketingChannel(MarketingChannelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True