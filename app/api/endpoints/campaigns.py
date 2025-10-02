from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import dependencies
from app.database import get_db
from app.crud.campaign import (
    get_campaign, get_campaigns, get_root_campaigns, get_campaigns_by_level,
    get_campaigns_by_parent, create_campaign, update_campaign, delete_campaign
)
from app.schemas.campaign import Campaign, CampaignCreate, CampaignUpdate

router = APIRouter()

@router.get("/", response_model=List[Campaign])
def read_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all campaigns"""
    campaigns = get_campaigns(db, skip=skip, limit=limit)
    return campaigns

@router.post("/", response_model=Campaign)
def create_new_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    """Create a new campaign"""
    return create_campaign(db=db, campaign=campaign)