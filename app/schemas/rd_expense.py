from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class RDExpenseBase(BaseModel):
    initiative_id: int
    expense_category: str  # Samples, Travel, Materials, Staffing, Marketing, Other
    expense_description: Optional[str] = None
    amount: float
    expense_date: date
    department: Optional[str] = None  # Marketing, Sales, Ops, Manufacturing
    cost_center: Optional[str] = None
    invoice_number: Optional[str] = None
    notes: Optional[str] = None


class RDExpenseCreate(RDExpenseBase):
    pass


class RDExpenseUpdate(BaseModel):
    expense_category: Optional[str] = None
    expense_description: Optional[str] = None
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None
    invoice_number: Optional[str] = None
    notes: Optional[str] = None


class RDExpense(RDExpenseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True