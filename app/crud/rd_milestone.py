from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.rd_initiative import RDMilestone
from app.schemas.rd_milestone import RDMilestoneCreate, RDMilestoneUpdate


def get_milestone(db: Session, milestone_id: int) -> Optional[RDMilestone]:
    """Get a single milestone"""
    return db.query(RDMilestone).filter(RDMilestone.id == milestone_id).first()


def get_milestones_by_initiative(
    db: Session,
    initiative_id: int,
    status: Optional[str] = None
) -> List[RDMilestone]:
    """Get all milestones for an initiative"""
    query = db.query(RDMilestone).filter(RDMilestone.initiative_id == initiative_id)
    
    if status:
        query = query.filter(RDMilestone.status == status)
    
    return query.order_by(RDMilestone.target_date).all()


def create_milestone(db: Session, milestone: RDMilestoneCreate) -> RDMilestone:
    """Create a new milestone"""
    db_milestone = RDMilestone(**milestone.model_dump())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone


def update_milestone(
    db: Session,
    milestone_id: int,
    milestone: RDMilestoneUpdate
) -> Optional[RDMilestone]:
    """Update milestone"""
    db_milestone = get_milestone(db, milestone_id)
    if not db_milestone:
        return None
    
    update_data = milestone.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_milestone, field, value)
    
    db.commit()
    db.refresh(db_milestone)
    return db_milestone


def delete_milestone(db: Session, milestone_id: int) -> bool:
    """Delete milestone"""
    db_milestone = get_milestone(db, milestone_id)
    if not db_milestone:
        return False
    
    db.delete(db_milestone)
    db.commit()
    return True