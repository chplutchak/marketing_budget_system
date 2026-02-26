from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

# ========================================
# Strategic Target Schemas
# ========================================

class StrategicTargetBase(BaseModel):
    year: int
    metric_name: str
    target_value: str
    delta_value: Optional[str] = None
    order_position: int = 0

class StrategicTargetCreate(StrategicTargetBase):
    pass

class StrategicTargetUpdate(BaseModel):
    metric_name: Optional[str] = None
    target_value: Optional[str] = None
    delta_value: Optional[str] = None
    order_position: Optional[int] = None

class StrategicTarget(StrategicTargetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ========================================
# Target Audience Schemas
# ========================================

class TargetAudienceBase(BaseModel):
    year: int
    priority: str
    audience_name: str
    color: Optional[str] = None
    icon: Optional[str] = None
    details: Optional[Dict] = None
    order_position: int = 0

class TargetAudienceCreate(TargetAudienceBase):
    pass

class TargetAudienceUpdate(BaseModel):
    priority: Optional[str] = None
    audience_name: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    details: Optional[Dict] = None
    order_position: Optional[int] = None

class TargetAudience(TargetAudienceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ========================================
# Marketing Objective Schemas
# ========================================

class MarketingObjectiveBase(BaseModel):
    year: int
    icon: Optional[str] = None
    title: str
    target: str
    measurement: str
    order_position: int = 0

class MarketingObjectiveCreate(MarketingObjectiveBase):
    pass

class MarketingObjectiveUpdate(BaseModel):
    icon: Optional[str] = None
    title: Optional[str] = None
    target: Optional[str] = None
    measurement: Optional[str] = None
    order_position: Optional[int] = None

class MarketingObjective(MarketingObjectiveBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True