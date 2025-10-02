from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.budget import (
    get_budget_item, get_budget_items, get_budget_items_by_campaign,
    get_budget_items_by_cost_center, get_budget_items_by_category,
    get_budget_items_with_relations, create_budget_item, 
    update_budget_item, delete_budget_item, get_budget_summary_by_campaign
)
from app.schemas.budget import BudgetItem, BudgetItemCreate, BudgetItemUpdate

router = APIRouter()

@router.get("/", response_model=List[BudgetItem])
def read_budget_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all budget items"""
    return get_budget_items(db, skip=skip, limit=limit)

@router.get("/with-relations")
def read_budget_items_with_relations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get budget items with campaign and cost center names"""
    results = get_budget_items_with_relations(db, skip=skip, limit=limit)
    
    # Transform the query results into proper response format
    items = []
    for budget_item, campaign_name, cost_center_name in results:
        item_dict = {
            "id": budget_item.id,
            "campaign_id": budget_item.campaign_id,
            "cost_center_id": budget_item.cost_center_id,
            "name": budget_item.name,
            "description": budget_item.description,
            "category": budget_item.category,
            "total_budget": budget_item.total_budget,
            "monthly_budget": budget_item.monthly_budget,
            "created_at": budget_item.created_at,
            "updated_at": budget_item.updated_at,
            "campaign_name": campaign_name,
            "cost_center_name": cost_center_name
        }
        items.append(item_dict)
    
    return items

@router.get("/campaign/{campaign_id}", response_model=List[BudgetItem])
def read_budget_items_by_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get all budget items for a specific campaign"""
    return get_budget_items_by_campaign(db, campaign_id=campaign_id)

@router.get("/cost-center/{cost_center_id}", response_model=List[BudgetItem])
def read_budget_items_by_cost_center(cost_center_id: int, db: Session = Depends(get_db)):
    """Get all budget items for a specific cost center"""
    return get_budget_items_by_cost_center(db, cost_center_id=cost_center_id)

@router.get("/category/{category}", response_model=List[BudgetItem])
def read_budget_items_by_category(category: str, db: Session = Depends(get_db)):
    """Get all budget items in a specific category"""
    return get_budget_items_by_category(db, category=category)

@router.get("/campaign/{campaign_id}/summary")
def get_campaign_budget_summary(campaign_id: int, db: Session = Depends(get_db)):
    """Get budget summary for a campaign"""
    return get_budget_summary_by_campaign(db, campaign_id=campaign_id)

@router.get("/{budget_item_id}", response_model=BudgetItem)
def read_budget_item(budget_item_id: int, db: Session = Depends(get_db)):
    """Get a specific budget item by ID"""
    budget_item = get_budget_item(db, budget_item_id=budget_item_id)
    if budget_item is None:
        raise HTTPException(status_code=404, detail="Budget item not found")
    return budget_item

@router.post("/", response_model=BudgetItem)
def create_new_budget_item(budget_item: BudgetItemCreate, db: Session = Depends(get_db)):
    """Create a new budget item"""
    # Verify campaign and cost center exist
    from app.crud.campaign import get_campaign
    from app.crud.cost_center import get_cost_center
    
    campaign = get_campaign(db, budget_item.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # We'll need to create cost center CRUD next, but for now let's skip this validation
    return create_budget_item(db=db, budget_item=budget_item)

@router.put("/{budget_item_id}", response_model=BudgetItem)
def update_budget_item_endpoint(budget_item_id: int, budget_update: BudgetItemUpdate, db: Session = Depends(get_db)):
    """Update an existing budget item"""
    budget_item = update_budget_item(db, budget_item_id=budget_item_id, budget_update=budget_update)
    if budget_item is None:
        raise HTTPException(status_code=404, detail="Budget item not found")
    return budget_item

@router.delete("/{budget_item_id}")
def delete_budget_item_endpoint(budget_item_id: int, db: Session = Depends(get_db)):
    """Delete a budget item"""
    success = delete_budget_item(db, budget_item_id=budget_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Budget item not found")
    return {"message": "Budget item deleted successfully"}