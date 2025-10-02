from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.crud.expense import (
    get_expense, get_expenses, get_expenses_by_budget_item,
    get_expenses_by_date_range, get_expenses_by_month,
    get_expenses_with_details, create_expense, update_expense,
    delete_expense, get_budget_vs_actual, get_campaign_spending_summary
)
from app.schemas.expense import ActualExpense, ActualExpenseCreate, ActualExpenseUpdate

router = APIRouter()

@router.get("/", response_model=List[ActualExpense])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all expenses"""
    return get_expenses(db, skip=skip, limit=limit)

@router.get("/with-details")
def read_expenses_with_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get expenses with budget item and campaign details"""
    results = get_expenses_with_details(db, skip=skip, limit=limit)
    
    expenses = []
    for expense, budget_item_name, campaign_name, category in results:
        expense_dict = {
            "id": expense.id,
            "budget_item_id": expense.budget_item_id,
            "amount": expense.amount,
            "expense_date": expense.expense_date,
            "description": expense.description,
            "vendor": expense.vendor,
            "invoice_number": expense.invoice_number,
            "payment_method": expense.payment_method,
            "approved_by": expense.approved_by,
            "approval_date": expense.approval_date,
            "created_at": expense.created_at,
            "updated_at": expense.updated_at,
            "budget_item_name": budget_item_name,
            "campaign_name": campaign_name,
            "category": category
        }
        expenses.append(expense_dict)
    
    return expenses

@router.get("/budget-item/{budget_item_id}", response_model=List[ActualExpense])
def read_expenses_by_budget_item(budget_item_id: int, db: Session = Depends(get_db)):
    """Get all expenses for a specific budget item"""
    return get_expenses_by_budget_item(db, budget_item_id=budget_item_id)

@router.get("/date-range")
def read_expenses_by_date_range(
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db)
):
    """Get expenses within a date range"""
    return get_expenses_by_date_range(db, start_date=start_date, end_date=end_date)

@router.get("/month/{year}/{month}")
def read_expenses_by_month(year: int, month: int, db: Session = Depends(get_db)):
    """Get all expenses for a specific month"""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
    return get_expenses_by_month(db, year=year, month=month)

@router.get("/variance/budget-item/{budget_item_id}")
def get_variance_analysis(
    budget_item_id: int,
    year: int = Query(..., description="Year"),
    month: int = Query(..., description="Month (1-12)"),
    db: Session = Depends(get_db)
):
    """Get budget vs actual variance for a budget item in a specific month"""
    result = get_budget_vs_actual(db, budget_item_id=budget_item_id, year=year, month=month)
    if result is None:
        raise HTTPException(status_code=404, detail="Budget item not found")
    return result

@router.get("/summary/campaign/{campaign_id}")
def get_campaign_summary(
    campaign_id: int,
    year: int = Query(None, description="Optional year filter"),
    db: Session = Depends(get_db)
):
    """Get spending summary for a campaign"""
    return get_campaign_spending_summary(db, campaign_id=campaign_id, year=year)

@router.get("/{expense_id}", response_model=ActualExpense)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    """Get a specific expense by ID"""
    expense = get_expense(db, expense_id=expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.post("/", response_model=ActualExpense)
def create_new_expense(expense: ActualExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense"""
    # Verify budget item exists
    from app.crud.budget import get_budget_item
    budget_item = get_budget_item(db, expense.budget_item_id)
    if not budget_item:
        raise HTTPException(status_code=404, detail="Budget item not found")
    
    return create_expense(db=db, expense=expense)

@router.put("/{expense_id}", response_model=ActualExpense)
def update_expense_endpoint(expense_id: int, expense_update: ActualExpenseUpdate, db: Session = Depends(get_db)):
    """Update an existing expense"""
    expense = update_expense(db, expense_id=expense_id, expense_update=expense_update)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.delete("/{expense_id}")
def delete_expense_endpoint(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense"""
    success = delete_expense(db, expense_id=expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}