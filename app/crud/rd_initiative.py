from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models.rd_initiative import RDInitiative
from app.schemas.rd_initiative import RDInitiativeCreate, RDInitiativeUpdate


def get_initiative(db: Session, initiative_id: int) -> Optional[RDInitiative]:
    """Get a single R&D initiative by ID"""
    return db.query(RDInitiative).filter(RDInitiative.id == initiative_id).first()


def get_initiatives(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    stage: Optional[str] = None,
    priority: Optional[str] = None,
    is_active: Optional[str] = None
) -> List[RDInitiative]:
    """Get all R&D initiatives with optional filters"""
    query = db.query(RDInitiative)
    
    if stage:
        query = query.filter(RDInitiative.stage == stage)
    if priority:
        query = query.filter(RDInitiative.priority == priority)
    if is_active:
        query = query.filter(RDInitiative.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()


def create_initiative(db: Session, initiative: RDInitiativeCreate) -> RDInitiative:
    """Create a new R&D initiative"""
    db_initiative = RDInitiative(**initiative.model_dump())
    db.add(db_initiative)
    db.commit()
    db.refresh(db_initiative)
    return db_initiative


def update_initiative(
    db: Session, 
    initiative_id: int, 
    initiative: RDInitiativeUpdate
) -> Optional[RDInitiative]:
    """Update an existing R&D initiative"""
    db_initiative = get_initiative(db, initiative_id)
    if not db_initiative:
        return None
    
    update_data = initiative.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_initiative, field, value)
    
    db.commit()
    db.refresh(db_initiative)
    return db_initiative


def delete_initiative(db: Session, initiative_id: int) -> bool:
    """Delete an R&D initiative"""
    db_initiative = get_initiative(db, initiative_id)
    if not db_initiative:
        return False
    
    db.delete(db_initiative)
    db.commit()
    return True


def get_initiative_with_details(db: Session, initiative_id: int) -> Optional[RDInitiative]:
    """Get initiative with all related data loaded"""
    return db.query(RDInitiative).filter(RDInitiative.id == initiative_id).first()