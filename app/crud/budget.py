from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.budget import BudgetItem
from app.models.campaign import Campaign
from app.models.cost_center import CostCenter
from app.schemas.budget import BudgetItemCreate, BudgetItemUpdate

def get_budget_item(db: Session, budget_item_id: int) -> Optional[BudgetItem]:
    return db.query(BudgetItem).filter(BudgetItem.id == budget_item_id).first()

def get_budget_items(db: Session, skip: int = 0, limit: int = 100) -> List[BudgetItem]:
    return db.query(BudgetItem).offset(skip).limit(limit).all()

def get_budget_items_by_campaign(db: Session, campaign_id: int) -> List[BudgetItem]:
    return db.query(BudgetItem).filter(BudgetItem.campaign_id == campaign_id).all()

def get_budget_items_by_cost_center(db: Session, cost_center_id: int) -> List[BudgetItem]:
    return db.query(BudgetItem).filter(BudgetItem.cost_center_id == cost_center_id).all()

def get_budget_items_by_category(db: Session, category: str) -> List[BudgetItem]:
    return db.query(BudgetItem).filter(BudgetItem.category == category).all()

def get_budget_items_with_relations(db: Session, skip: int = 0, limit: int = 100):
    """Get budget items with campaign and cost center names"""
    return (
        db.query(
            BudgetItem,
            Campaign.name.label('campaign_name'),
            CostCenter.name.label('cost_center_name')
        )
        .join(Campaign, BudgetItem.campaign_id == Campaign.id)
        .join(CostCenter, BudgetItem.cost_center_id == CostCenter.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_budget_item(db: Session, budget_item: BudgetItemCreate) -> BudgetItem:
    # Convert monthly_budget to proper JSON format if it exists
    monthly_budget_json = None
    if budget_item.monthly_budget:
        # Ensure keys are strings for JSON storage
        monthly_budget_json = {str(k): float(v) for k, v in budget_item.monthly_budget.items()}
    
    db_budget_item = BudgetItem(
        campaign_id=budget_item.campaign_id,
        cost_center_id=budget_item.cost_center_id,
        name=budget_item.name,
        description=budget_item.description,
        category=budget_item.category,
        total_budget=budget_item.total_budget,
        monthly_budget=monthly_budget_json
    )
    
    db.add(db_budget_item)
    db.commit()
    db.refresh(db_budget_item)
    return db_budget_item

def update_budget_item(db: Session, budget_item_id: int, budget_update: BudgetItemUpdate) -> Optional[BudgetItem]:
    db_budget_item = db.query(BudgetItem).filter(BudgetItem.id == budget_item_id).first()
    if db_budget_item:
        update_data = budget_update.dict(exclude_unset=True)
        
        # Handle monthly_budget conversion
        if 'monthly_budget' in update_data and update_data['monthly_budget']:
            update_data['monthly_budget'] = {str(k): float(v) for k, v in update_data['monthly_budget'].items()}
        
        for field, value in update_data.items():
            setattr(db_budget_item, field, value)
        
        db.commit()
        db.refresh(db_budget_item)
    return db_budget_item

def delete_budget_item(db: Session, budget_item_id: int) -> bool:
    db_budget_item = db.query(BudgetItem).filter(BudgetItem.id == budget_item_id).first()
    if db_budget_item:
        db.delete(db_budget_item)
        db.commit()
        return True
    return False

def get_budget_summary_by_campaign(db: Session, campaign_id: int):
    """Get budget summary for a campaign"""
    budget_items = get_budget_items_by_campaign(db, campaign_id)
    
    if not budget_items:
        return {
            "campaign_id": campaign_id,
            "total_budget": 0.0,
            "item_count": 0,
            "categories": {}
        }
    
    total_budget = sum(item.total_budget for item in budget_items)
    categories = {}
    
    for item in budget_items:
        if item.category not in categories:
            categories[item.category] = {
                "count": 0,
                "total_budget": 0.0
            }
        categories[item.category]["count"] += 1
        categories[item.category]["total_budget"] += item.total_budget
    
    return {
        "campaign_id": campaign_id,
        "total_budget": total_budget,
        "item_count": len(budget_items),
        "categories": categories
    }