from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class BudgetItem(Base):
    __tablename__ = "budget_items"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    
    # Budget details
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)  # e.g., "Digital Ads", "Personnel", "Events"
    
    # Budget amounts
    total_budget = Column(Float, nullable=False, default=0.0)
    
    # Monthly budget distribution (JSON: {1: 1000, 2: 1500, ...} for months 1-12)
    monthly_budget = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    campaign = relationship("Campaign", back_populates="budget_items")
    cost_center = relationship("CostCenter", back_populates="budget_items")
    actual_expenses = relationship("ActualExpense", back_populates="budget_item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BudgetItem(name='{self.name}', budget=${self.total_budget})>"