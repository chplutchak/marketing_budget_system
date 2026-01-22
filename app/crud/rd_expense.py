from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.rd_initiative import RDExpense
from app.schemas.rd_expense import RDExpenseCreate, RDExpenseUpdate


def get_expense(db: Session, expense_id: int) -> Optional[RDExpense]:
    """Get a single expense"""
    return db.query(RDExpense).filter(RDExpense.id == expense_id).first()


def get_expenses_by_initiative(
    db: Session, 
    initiative_id: int,
    category: Optional[str] = None,
    department: Optional[str] = None
) -> List[RDExpense]:
    """Get all expenses for an initiative with optional filters"""
    query = db.query(RDExpense).filter(RDExpense.initiative_id == initiative_id)
    
    if category:
        query = query.filter(RDExpense.expense_category == category)
    if department:
        query = query.filter(RDExpense.department == department)
    
    return query.all()


def create_expense(db: Session, expense: RDExpenseCreate) -> RDExpense:
    """Create a new expense"""
    db_expense = RDExpense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(
    db: Session,
    expense_id: int,
    expense: RDExpenseUpdate
) -> Optional[RDExpense]:
    """Update expense"""
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return None
    
    update_data = expense.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_expense, field, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int) -> bool:
    """Delete expense"""
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return False
    
    db.delete(db_expense)
    db.commit()
    return True


def get_total_expenses(db: Session, initiative_id: int) -> float:
    """Calculate total expenses for an initiative"""
    expenses = get_expenses_by_initiative(db, initiative_id)
    return sum(exp.amount for exp in expenses)