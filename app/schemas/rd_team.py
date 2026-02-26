"""
Create this new file: app/schemas/rd_team.py
"""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDInitiativeTeamBase(BaseModel):
    initiative_id: int
    department: str  # Marketing, Operations, Manufacturing, Sales, R&D
    person_name: str
    role: Optional[str] = None  # Lead, Support, Reviewer, Stakeholder


class RDInitiativeTeamCreate(RDInitiativeTeamBase):
    pass


class RDInitiativeTeamUpdate(BaseModel):
    department: Optional[str] = None
    person_name: Optional[str] = None
    role: Optional[str] = None


class RDInitiativeTeam(RDInitiativeTeamBase):
    id: int
    assigned_date: date
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True