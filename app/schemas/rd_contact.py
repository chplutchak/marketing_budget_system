from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDContactBase(BaseModel):
    initiative_id: int
    contact_date: date
    contact_type: str  # email, call, meeting, convention, demo
    contact_person: Optional[str] = None
    company: Optional[str] = None
    utak_contact: Optional[str] = None
    department: Optional[str] = None  # sales, marketing, ops, manufacturing
    subject: Optional[str] = None
    notes: Optional[str] = None
    outcome: Optional[str] = None  # positive, neutral, negative, needs_follow_up
    next_action: Optional[str] = None
    next_action_date: Optional[date] = None
    next_action_owner: Optional[str] = None


class RDContactCreate(RDContactBase):
    pass


class RDContactUpdate(BaseModel):
    contact_date: Optional[date] = None
    contact_type: Optional[str] = None
    contact_person: Optional[str] = None
    company: Optional[str] = None
    utak_contact: Optional[str] = None
    department: Optional[str] = None
    subject: Optional[str] = None
    notes: Optional[str] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[date] = None
    next_action_owner: Optional[str] = None


class RDContact(RDContactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True