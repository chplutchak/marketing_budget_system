from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate

def get_campaign(db: Session, campaign_id: int) -> Optional[Campaign]:
    return db.query(Campaign).filter(Campaign.id == campaign_id).first()

def get_campaigns(db: Session, skip: int = 0, limit: int = 100) -> List[Campaign]:
    return db.query(Campaign).offset(skip).limit(limit).all()

def get_campaigns_by_level(db: Session, level: int) -> List[Campaign]:
    return db.query(Campaign).filter(Campaign.level == level).all()

def get_campaigns_by_parent(db: Session, parent_id: int) -> List[Campaign]:
    return db.query(Campaign).filter(Campaign.parent_id == parent_id).all()

def get_root_campaigns(db: Session) -> List[Campaign]:
    return db.query(Campaign).filter(Campaign.parent_id.is_(None)).all()

def create_campaign(db: Session, campaign: CampaignCreate) -> Campaign:
    db_campaign = Campaign(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def update_campaign(db: Session, campaign_id: int, campaign_update: CampaignUpdate) -> Optional[Campaign]:
    db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if db_campaign:
        update_data = campaign_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_campaign, field, value)
        db.commit()
        db.refresh(db_campaign)
    return db_campaign

def delete_campaign(db: Session, campaign_id: int) -> bool:
    db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if db_campaign:
        db.delete(db_campaign)
        db.commit()
        return True
    return False

def get_campaign_hierarchy(db: Session, root_campaign_id: int) -> Optional[Campaign]:
    """Get a campaign with all its children (recursive)"""
    campaign = db.query(Campaign).filter(Campaign.id == root_campaign_id).first()
    return campaign  # SQLAlchemy will automatically load children via relationships