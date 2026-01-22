from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDNoteBase(BaseModel):
    initiative_id: int
    department: Optional[str] = None  # Marketing, Sales, Ops, Manufacturing
    author: str
    note_category: Optional[str] = None  # General, Technical, Customer Feedback, Action Item
    note_text: str


class RDNoteCreate(RDNoteBase):
    pass


class RDNoteUpdate(BaseModel):
    note_text: Optional[str] = None
    note_category: Optional[str] = None


class RDNote(RDNoteBase):
    id: int
    note_date: date
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True