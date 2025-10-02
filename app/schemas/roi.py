from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date, datetime

class ROIMetricBase(BaseModel):
    calculation_date: date
    period_start: date
    period_end: date
    total_cost: float = 0.0
    revenue_attributed: float = 0.0
    performance_metrics: Optional[Dict[str, float]] = None  # e.g., {"leads": 150, "conversions": 25}
    attribution_method: str = "last_touch"
    attribution_notes: Optional[str] = None

class ROIMetricCreate(ROIMetricBase):
    campaign_id: int

class ROIMetricUpdate(BaseModel):
    total_cost: Optional[float] = None
    revenue_attributed: Optional[float] = None
    performance_metrics: Optional[Dict[str, float]] = None
    attribution_notes: Optional[str] = None

class ROIMetric(ROIMetricBase):
    id: int
    campaign_id: int
    roi_percentage: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ROIMetricWithCampaign(ROIMetric):
    campaign_name: Optional[str] = None
    
    class Config:
        from_attributes = True