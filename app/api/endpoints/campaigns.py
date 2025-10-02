from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.campaign import (
    get_campaign, get_campaigns, get_root_campaigns, get_campaigns_by_level,
    get_campaigns_by_parent, create_campaign, update_campaign, delete_campaign,
    get_budget_allocation
)
from app.schemas.campaign import Campaign, CampaignCreate, CampaignUpdate

router = APIRouter()

@router.get("/", response_model=List[Campaign])
def read_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all campaigns"""
    campaigns = get_campaigns(db, skip=skip, limit=limit)
    return campaigns

@router.get("/root", response_model=List[Campaign])
def read_root_campaigns(db: Session = Depends(get_db)):
    """Get all root campaigns (top-level campaigns with no parent)"""
    campaigns = get_root_campaigns(db)
    return campaigns

@router.get("/level/{level}", response_model=List[Campaign])
def read_campaigns_by_level(level: int, db: Session = Depends(get_db)):
    """Get all campaigns at a specific level"""
    campaigns = get_campaigns_by_level(db, level=level)
    return campaigns

@router.get("/{campaign_id}", response_model=Campaign)
def read_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get a specific campaign by ID"""
    db_campaign = get_campaign(db, campaign_id=campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

@router.get("/{campaign_id}/budget-allocation")
def get_campaign_budget_allocation(campaign_id: int, db: Session = Depends(get_db)):
    """Get budget allocation status for a campaign"""
    result = get_budget_allocation(db, campaign_id=campaign_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return result

@router.get("/{parent_id}/children", response_model=List[Campaign])
def read_campaign_children(parent_id: int, db: Session = Depends(get_db)):
    """Get all children of a specific campaign"""
    children = get_campaigns_by_parent(db, parent_id=parent_id)
    return children

@router.post("/", response_model=Campaign)
def create_new_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    """Create a new campaign"""
    return create_campaign(db=db, campaign=campaign)

@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign_endpoint(campaign_id: int, campaign_update: CampaignUpdate, db: Session = Depends(get_db)):
    """Update an existing campaign"""
    db_campaign = update_campaign(db, campaign_id=campaign_id, campaign_update=campaign_update)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

@router.delete("/{campaign_id}")
def delete_campaign_endpoint(campaign_id: int, db: Session = Depends(get_db)):
    """Delete a campaign"""
    success = delete_campaign(db, campaign_id=campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}