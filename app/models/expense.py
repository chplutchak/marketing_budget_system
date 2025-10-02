from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ActualExpense(Base):
    __tablename__ = "actual_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    budget_item_id = Column(Integer, ForeignKey("budget_items.id"), nullable=False)
    
    # Expense details
    amount = Column(Float, nullable=False)
    expense_date = Column(Date, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Optional tracking fields
    vendor = Column(String(255), nullable=True)
    invoice_number = Column(String(100), nullable=True)
    payment_method = Column(String(50), nullable=True)  # e.g., "Credit Card", "Check", "ACH"
    
    # Approval tracking
    approved_by = Column(String(255), nullable=True)
    approval_date = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    budget_item = relationship("BudgetItem", back_populates="actual_expenses")
    
    def __repr__(self):
        return f"<ActualExpense(amount=${self.amount}, date={self.expense_date})>"