from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class MarketingBudget(Base):
    """Overall marketing budget for a year"""
    __tablename__ = "marketing_budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, unique=True, index=True)
    
    # Total budget breakdown
    total_budget = Column(Float, nullable=False)
    fixed_costs = Column(Float, nullable=False)
    flexible_budget = Column(Float, nullable=False)
    
    # Fixed costs detail (JSON)
    # {"CaliNetworks": 24450, "Conventions": 40711, "HubSpot": 26875, "Designer": 23196}
    fixed_costs_detail = Column(JSON, nullable=True)
    
    # Flexible budget detail (JSON)
    # {"Convention Support": 30000, "R&D / Direct Mail": 30000, ...}
    flexible_budget_detail = Column(JSON, nullable=True)
    
    # Quarterly distribution (JSON)
    # {"Q1": {"total": 48300, "focus": "..."}, "Q2": {...}, ...}
    quarterly_distribution = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<MarketingBudget(year={self.year}, total=${self.total_budget})>"


class BudgetCategory(Base):
    """Individual budget categories with details"""
    __tablename__ = "budget_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, nullable=False)  # References MarketingBudget
    year = Column(Integer, nullable=False, index=True)
    
    # Category details
    category_type = Column(String(50), nullable=False)  # "fixed" or "flexible"
    category_name = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    color = Column(String(20), nullable=True)  # Hex color for card display
    description = Column(String(500), nullable=True)
    
    # Breakdown details (JSON) - for subcategories
    # e.g., {"Materials": 25000, "Pre/post campaigns": 5000}
    breakdown = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<BudgetCategory(name='{self.category_name}', amount=${self.amount})>"