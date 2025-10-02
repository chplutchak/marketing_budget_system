from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from typing import List, Optional
from datetime import date, datetime
from app.models.expense import ActualExpense
from app.models.budget import BudgetItem
from app.models.campaign import Campaign
from app.schemas.expense import ActualExpenseCreate, ActualExpenseUpdate

def get_expense(db: Session, expense_id: int) -> Optional[ActualExpense]:
    return db.query(ActualExpense).filter(ActualExpense.id == expense_id).first()

def get_expenses(db: Session, skip: int = 0, limit: int = 100) -> List[ActualExpense]:
    return db.query(ActualExpense).offset(skip).limit(limit).all()

def get_expenses_by_budget_item(db: Session, budget_item_id: int) -> List[ActualExpense]:
    return db.query(ActualExpense).filter(ActualExpense.budget_item_id == budget_item_id).all()

def get_expenses_by_date_range(db: Session, start_date: date, end_date: date) -> List[ActualExpense]:
    return db.query(ActualExpense).filter(
        ActualExpense.expense_date >= start_date,
        ActualExpense.expense_date <= end_date
    ).all()

def get_expenses_by_month(db: Session, year: int, month: int) -> List[ActualExpense]:
    return db.query(ActualExpense).filter(
        extract('year', ActualExpense.expense_date) == year,
        extract('month', ActualExpense.expense_date) == month
    ).all()

def get_expenses_with_details(db: Session, skip: int = 0, limit: int = 100):
    """Get expenses with budget item, campaign, and category information"""
    return (
        db.query(
            ActualExpense,
            BudgetItem.name.label('budget_item_name'),
            Campaign.name.label('campaign_name'),
            BudgetItem.category.label('category')
        )
        .join(BudgetItem, ActualExpense.budget_item_id == BudgetItem.id)
        .join(Campaign, BudgetItem.campaign_id == Campaign.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_expense(db: Session, expense: ActualExpenseCreate) -> ActualExpense:
    db_expense = ActualExpense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def update_expense(db: Session, expense_id: int, expense_update: ActualExpenseUpdate) -> Optional[ActualExpense]:
    db_expense = db.query(ActualExpense).filter(ActualExpense.id == expense_id).first()
    if db_expense:
        update_data = expense_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_expense, field, value)
        db.commit()
        db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int) -> bool:
    db_expense = db.query(ActualExpense).filter(ActualExpense.id == expense_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
        return True
    return False

def get_budget_vs_actual(db: Session, budget_item_id: int, year: int, month: int):
    """Compare budgeted vs actual spending for a specific month"""
    # Get budget item
    budget_item = db.query(BudgetItem).filter(BudgetItem.id == budget_item_id).first()
    if not budget_item:
        return None
    
    # Get budgeted amount for this month
    monthly_budget = 0.0
    if budget_item.monthly_budget and str(month) in budget_item.monthly_budget:
        monthly_budget = float(budget_item.monthly_budget[str(month)])
    
    # Get actual expenses for this month
    expenses = get_expenses_by_month(db, year, month)
    budget_expenses = [e for e in expenses if e.budget_item_id == budget_item_id]
    actual_total = sum(e.amount for e in budget_expenses)
    
    variance = actual_total - monthly_budget
    variance_pct = (variance / monthly_budget * 100) if monthly_budget > 0 else 0
    
    return {
        "budget_item_id": budget_item_id,
        "budget_item_name": budget_item.name,
        "year": year,
        "month": month,
        "budgeted": monthly_budget,
        "actual": actual_total,
        "variance": variance,
        "variance_percentage": variance_pct,
        "over_budget": variance > 0
    }

def get_campaign_spending_summary(db: Session, campaign_id: int, year: int = None):
    """Get total spending for a campaign"""
    # Get all budget items for this campaign
    budget_items = db.query(BudgetItem).filter(BudgetItem.campaign_id == campaign_id).all()
    budget_item_ids = [bi.id for bi in budget_items]
    
    # Get all expenses for these budget items
    query = db.query(ActualExpense).filter(ActualExpense.budget_item_id.in_(budget_item_ids))
    
    if year:
        query = query.filter(extract('year', ActualExpense.expense_date) == year)
    
    expenses = query.all()
    
    total_budgeted = sum(bi.total_budget for bi in budget_items)
    total_actual = sum(e.amount for e in expenses)
    
    return {
        "campaign_id": campaign_id,
        "year": year,
        "total_budgeted": total_budgeted,
        "total_actual": total_actual,
        "variance": total_actual - total_budgeted,
        "variance_percentage": ((total_actual - total_budgeted) / total_budgeted * 100) if total_budgeted > 0 else 0,
        "expense_count": len(expenses)
    }