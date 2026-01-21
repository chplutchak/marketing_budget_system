from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# ==================== KPI METRIC SCHEMAS ====================

class KPIMetricBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    baseline_value: Optional[float] = None
    baseline_label: Optional[str] = None
    target_value: float
    target_label: str
    measurement_method: str
    tracking_frequency: str
    unit: Optional[str] = None
    target_threshold_high: float = 0.95
    target_threshold_low: float = 0.70

class KPIMetricCreate(KPIMetricBase):
    pass

class KPIMetricUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    baseline_value: Optional[float] = None
    baseline_label: Optional[str] = None
    target_value: Optional[float] = None
    target_label: Optional[str] = None
    measurement_method: Optional[str] = None
    tracking_frequency: Optional[str] = None
    unit: Optional[str] = None
    target_threshold_high: Optional[float] = None
    target_threshold_low: Optional[float] = None
    is_active: Optional[str] = None

class KPIMetricResponse(KPIMetricBase):
    id: int
    is_active: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ==================== KPI SNAPSHOT SCHEMAS ====================

class KPISnapshotBase(BaseModel):
    metric_id: int
    snapshot_date: date
    snapshot_type: str  # "weekly" or "monthly"
    actual_value: float
    notes: Optional[str] = None

class KPISnapshotCreate(KPISnapshotBase):
    pass

class KPISnapshotResponse(KPISnapshotBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True