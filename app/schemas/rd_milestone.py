from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDMilestoneBase(BaseModel):
    initiative_id: int
    milestone_name: str
    milestone_type: str  # feasibility_complete, samples_ready, validation_done, launch_materials_ready, launched
    target_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: str = "not_started"  # not_started, in_progress, completed, delayed, blocked
    owner: Optional[str] = None
    notes: Optional[str] = None
    blockers: Optional[str] = None


class RDMilestoneCreate(RDMilestoneBase):
    pass


class RDMilestoneUpdate(BaseModel):
    milestone_name: Optional[str] = None
    milestone_type: Optional[str] = None
    target_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    notes: Optional[str] = None
    blockers: Optional[str] = None


class RDMilestone(RDMilestoneBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True