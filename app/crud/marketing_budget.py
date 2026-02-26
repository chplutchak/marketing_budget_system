from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.marketing_budget import MarketingBudget, BudgetCategory
from app.schemas.marketing_budget import (
    MarketingBudgetCreate, MarketingBudgetUpdate,
    BudgetCategoryCreate, BudgetCategoryUpdate
)

# ========================================
# Marketing Budget CRUD
# ========================================

def get_budget(db: Session, budget_id: int) -> Optional[MarketingBudget]:
    """Get a specific budget by ID"""
    return db.query(MarketingBudget).filter(MarketingBudget.id == budget_id).first()

def get_budget_by_year(db: Session, year: int) -> Optional[MarketingBudget]:
    """Get budget for a specific year"""
    return db.query(MarketingBudget).filter(MarketingBudget.year == year).first()

def get_all_budgets(db: Session, skip: int = 0, limit: int = 100) -> List[MarketingBudget]:
    """Get all budgets"""
    return db.query(MarketingBudget).order_by(
        MarketingBudget.year.desc()
    ).offset(skip).limit(limit).all()

def create_budget(db: Session, budget: MarketingBudgetCreate) -> MarketingBudget:
    """Create a new budget"""
    db_budget = MarketingBudget(**budget.model_dump())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def update_budget(db: Session, budget_id: int, budget_update: MarketingBudgetUpdate) -> Optional[MarketingBudget]:
    """Update an existing budget"""
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        return None
    
    update_data = budget_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    
    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int) -> bool:
    """Delete a budget"""
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        return False
    
    db.delete(db_budget)
    db.commit()
    return True

# ========================================
# Budget Category CRUD
# ========================================

def get_category(db: Session, category_id: int) -> Optional[BudgetCategory]:
    """Get a specific category by ID"""
    return db.query(BudgetCategory).filter(BudgetCategory.id == category_id).first()

def get_categories_by_budget(db: Session, budget_id: int) -> List[BudgetCategory]:
    """Get all categories for a budget"""
    return db.query(BudgetCategory).filter(
        BudgetCategory.budget_id == budget_id
    ).all()

def get_categories_by_year(db: Session, year: int) -> List[BudgetCategory]:
    """Get all categories for a year"""
    return db.query(BudgetCategory).filter(
        BudgetCategory.year == year
    ).all()

def get_categories_by_type(db: Session, budget_id: int, category_type: str) -> List[BudgetCategory]:
    """Get categories by type (fixed or flexible)"""
    return db.query(BudgetCategory).filter(
        BudgetCategory.budget_id == budget_id,
        BudgetCategory.category_type == category_type
    ).all()

def create_category(db: Session, category: BudgetCategoryCreate) -> BudgetCategory:
    """Create a new category"""
    db_category = BudgetCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def create_multiple_categories(db: Session, categories: List[BudgetCategoryCreate]) -> List[BudgetCategory]:
    """Create multiple categories at once"""
    db_categories = [BudgetCategory(**category.model_dump()) for category in categories]
    db.add_all(db_categories)
    db.commit()
    for category in db_categories:
        db.refresh(category)
    return db_categories

def update_category(db: Session, category_id: int, category_update: BudgetCategoryUpdate) -> Optional[BudgetCategory]:
    """Update an existing category"""
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    
    update_data = category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    """Delete a category"""
    db_category = get_category(db, category_id)
    if not db_category:
        return False
    
    db.delete(db_category)
    db.commit()
    return True