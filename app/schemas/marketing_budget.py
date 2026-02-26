from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

# ========================================
# Marketing Budget Schemas
# ========================================

class MarketingBudgetBase(BaseModel):
    year: int
    total_budget: float
    fixed_costs: float
    flexible_budget: float
    fixed_costs_detail: Optional[Dict[str, float]] = None
    flexible_budget_detail: Optional[Dict[str, float]] = None
    quarterly_distribution: Optional[Dict[str, Dict]] = None

class MarketingBudgetCreate(MarketingBudgetBase):
    pass

class MarketingBudgetUpdate(BaseModel):
    total_budget: Optional[float] = None
    fixed_costs: Optional[float] = None
    flexible_budget: Optional[float] = None
    fixed_costs_detail: Optional[Dict[str, float]] = None
    flexible_budget_detail: Optional[Dict[str, float]] = None
    quarterly_distribution: Optional[Dict[str, Dict]] = None

class MarketingBudget(MarketingBudgetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ========================================
# Budget Category Schemas
# ========================================

class BudgetCategoryBase(BaseModel):
    year: int
    category_type: str  # "fixed" or "flexible"
    category_name: str
    amount: float
    color: Optional[str] = None
    description: Optional[str] = None
    breakdown: Optional[Dict[str, float]] = None

class BudgetCategoryCreate(BudgetCategoryBase):
    budget_id: int

class BudgetCategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    amount: Optional[float] = None
    color: Optional[str] = None
    description: Optional[str] = None
    breakdown: Optional[Dict[str, float]] = None

class BudgetCategory(BudgetCategoryBase):
    id: int
    budget_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ========================================
# Combined Response
# ========================================

class MarketingBudgetWithCategories(MarketingBudget):
    categories: list[BudgetCategory] = []
    
    class Config:
        from_attributes = True