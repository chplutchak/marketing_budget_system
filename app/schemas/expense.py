from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ActualExpenseBase(BaseModel):
    amount: float
    expense_date: date
    description: Optional[str] = None
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    payment_method: Optional[str] = None

class ActualExpenseCreate(ActualExpenseBase):
    budget_item_id: int

class ActualExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    description: Optional[str] = None
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    payment_method: Optional[str] = None
    approved_by: Optional[str] = None
    approval_date: Optional[date] = None

class ActualExpense(ActualExpenseBase):
    id: int
    budget_item_id: int
    approved_by: Optional[str] = None
    approval_date: Optional[date] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ActualExpenseWithDetails(ActualExpense):
    budget_item_name: Optional[str] = None
    campaign_name: Optional[str] = None
    category: Optional[str] = None
    
    class Config:
        from_attributes = True