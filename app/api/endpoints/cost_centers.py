from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.cost_center import (
    get_cost_center, get_cost_center_by_code, get_cost_centers,
    get_active_cost_centers, get_cost_centers_by_department,
    create_cost_center, update_cost_center, delete_cost_center
)
from app.schemas.cost_center import CostCenter, CostCenterCreate, CostCenterUpdate

router = APIRouter()

@router.get("/", response_model=List[CostCenter])
def read_cost_centers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all cost centers"""
    return get_cost_centers(db, skip=skip, limit=limit)

@router.get("/active", response_model=List[CostCenter])
def read_active_cost_centers(db: Session = Depends(get_db)):
    """Get all active cost centers"""
    return get_active_cost_centers(db)

@router.get("/department/{department}", response_model=List[CostCenter])
def read_cost_centers_by_department(department: str, db: Session = Depends(get_db)):
    """Get all cost centers for a specific department"""
    return get_cost_centers_by_department(db, department=department)

@router.get("/code/{code}", response_model=CostCenter)
def read_cost_center_by_code(code: str, db: Session = Depends(get_db)):
    """Get a cost center by its code"""
    cost_center = get_cost_center_by_code(db, code=code)
    if cost_center is None:
        raise HTTPException(status_code=404, detail="Cost center not found")
    return cost_center

@router.get("/{cost_center_id}", response_model=CostCenter)
def read_cost_center(cost_center_id: int, db: Session = Depends(get_db)):
    """Get a specific cost center by ID"""
    cost_center = get_cost_center(db, cost_center_id=cost_center_id)
    if cost_center is None:
        raise HTTPException(status_code=404, detail="Cost center not found")
    return cost_center

@router.post("/", response_model=CostCenter)
def create_new_cost_center(cost_center: CostCenterCreate, db: Session = Depends(get_db)):
    """Create a new cost center"""
    # Check if code already exists
    existing = get_cost_center_by_code(db, cost_center.code)
    if existing:
        raise HTTPException(status_code=400, detail="Cost center with this code already exists")
    
    return create_cost_center(db=db, cost_center=cost_center)

@router.put("/{cost_center_id}", response_model=CostCenter)
def update_cost_center_endpoint(cost_center_id: int, cost_center_update: CostCenterUpdate, db: Session = Depends(get_db)):
    """Update an existing cost center"""
    # If updating code, check it doesn't conflict with existing ones
    if cost_center_update.code:
        existing = get_cost_center_by_code(db, cost_center_update.code)
        if existing and existing.id != cost_center_id:
            raise HTTPException(status_code=400, detail="Cost center with this code already exists")
    
    cost_center = update_cost_center(db, cost_center_id=cost_center_id, cost_center_update=cost_center_update)
    if cost_center is None:
        raise HTTPException(status_code=404, detail="Cost center not found")
    return cost_center

@router.delete("/{cost_center_id}")
def delete_cost_center_endpoint(cost_center_id: int, db: Session = Depends(get_db)):
    """Deactivate a cost center (soft delete)"""
    success = delete_cost_center(db, cost_center_id=cost_center_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cost center not found")
    return {"message": "Cost center deactivated successfully"}