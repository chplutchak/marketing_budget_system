from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.marketing_budget import (
    get_budget, get_budget_by_year, get_all_budgets,
    create_budget, update_budget, delete_budget,
    get_category, get_categories_by_budget, get_categories_by_year,
    get_categories_by_type, create_category, create_multiple_categories,
    update_category, delete_category
)
from app.schemas.marketing_budget import (
    MarketingBudget, MarketingBudgetCreate, MarketingBudgetUpdate,
    BudgetCategory, BudgetCategoryCreate, BudgetCategoryUpdate
)

router = APIRouter()

# ========================================
# Budget Endpoints
# ========================================

@router.get("/budgets/", response_model=List[MarketingBudget])
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all budgets"""
    return get_all_budgets(db, skip=skip, limit=limit)

@router.get("/budgets/year/{year}", response_model=MarketingBudget)
def read_budget_by_year(year: int, db: Session = Depends(get_db)):
    """Get budget for a specific year"""
    budget = get_budget_by_year(db, year=year)
    if not budget:
        raise HTTPException(status_code=404, detail=f"Budget for {year} not found")
    return budget

@router.get("/budgets/{budget_id}", response_model=MarketingBudget)
def read_budget(budget_id: int, db: Session = Depends(get_db)):
    """Get a specific budget by ID"""
    budget = get_budget(db, budget_id=budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.post("/budgets/", response_model=MarketingBudget)
def create_new_budget(budget: MarketingBudgetCreate, db: Session = Depends(get_db)):
    """Create a new budget"""
    # Check if budget already exists for this year
    existing = get_budget_by_year(db, year=budget.year)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Budget for {budget.year} already exists"
        )
    return create_budget(db=db, budget=budget)

@router.put("/budgets/{budget_id}", response_model=MarketingBudget)
def update_budget_endpoint(
    budget_id: int,
    budget_update: MarketingBudgetUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing budget"""
    budget = update_budget(db, budget_id=budget_id, budget_update=budget_update)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.delete("/budgets/{budget_id}")
def delete_budget_endpoint(budget_id: int, db: Session = Depends(get_db)):
    """Delete a budget"""
    success = delete_budget(db, budget_id=budget_id)
    if not success:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"message": "Budget deleted successfully"}

# ========================================
# Category Endpoints
# ========================================

@router.get("/categories/{category_id}", response_model=BudgetCategory)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    category = get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/categories/budget/{budget_id}", response_model=List[BudgetCategory])
def read_categories_by_budget(budget_id: int, db: Session = Depends(get_db)):
    """Get all categories for a budget"""
    budget = get_budget(db, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return get_categories_by_budget(db, budget_id=budget_id)

@router.get("/categories/year/{year}", response_model=List[BudgetCategory])
def read_categories_by_year(year: int, db: Session = Depends(get_db)):
    """Get all categories for a year"""
    return get_categories_by_year(db, year=year)

@router.get("/categories/budget/{budget_id}/type/{category_type}", response_model=List[BudgetCategory])
def read_categories_by_type(budget_id: int, category_type: str, db: Session = Depends(get_db)):
    """Get categories by type (fixed or flexible)"""
    if category_type not in ["fixed", "flexible"]:
        raise HTTPException(status_code=400, detail="Category type must be 'fixed' or 'flexible'")
    return get_categories_by_type(db, budget_id=budget_id, category_type=category_type)

@router.post("/categories/", response_model=BudgetCategory)
def create_new_category(category: BudgetCategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    # Verify budget exists
    budget = get_budget(db, category.budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return create_category(db=db, category=category)

@router.post("/categories/bulk", response_model=List[BudgetCategory])
def create_bulk_categories(categories: List[BudgetCategoryCreate], db: Session = Depends(get_db)):
    """Create multiple categories at once"""
    if not categories:
        raise HTTPException(status_code=400, detail="No categories provided")
    
    # Verify all budgets exist
    budget_ids = set(c.budget_id for c in categories)
    for budget_id in budget_ids:
        budget = get_budget(db, budget_id)
        if not budget:
            raise HTTPException(status_code=404, detail=f"Budget {budget_id} not found")
    
    return create_multiple_categories(db=db, categories=categories)

@router.put("/categories/{category_id}", response_model=BudgetCategory)
def update_category_endpoint(
    category_id: int,
    category_update: BudgetCategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing category"""
    category = update_category(db, category_id=category_id, category_update=category_update)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}")
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    """Delete a category"""
    success = delete_category(db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}