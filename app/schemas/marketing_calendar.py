from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ========================================
# Marketing Calendar Schemas
# ========================================

class MarketingCalendarBase(BaseModel):
    year: int
    month: int  # 1-12
    focus: Optional[str] = None
    major_campaigns: Optional[List[str]] = None

class MarketingCalendarCreate(MarketingCalendarBase):
    pass

class MarketingCalendarUpdate(BaseModel):
    focus: Optional[str] = None
    major_campaigns: Optional[List[str]] = None

class MarketingCalendar(MarketingCalendarBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ========================================
# Marketing Activity Schemas
# ========================================

class MarketingActivityBase(BaseModel):
    week_number: int  # 1-4
    activity_name: str
    day_of_week: str  # monday, tuesday, wednesday, thursday, friday
    order_in_week: int = 0
    is_completed: bool = False

class MarketingActivityCreate(MarketingActivityBase):
    calendar_id: int

class MarketingActivityUpdate(BaseModel):
    activity_name: Optional[str] = None
    day_of_week: Optional[str] = None
    order_in_week: Optional[int] = None
    is_completed: Optional[bool] = None

class MarketingActivity(MarketingActivityBase):
    id: int
    calendar_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ========================================
# Combined Response
# ========================================

class MarketingCalendarWithActivities(MarketingCalendar):
    activities: List[MarketingActivity] = []
    
    class Config:
        from_attributes = True