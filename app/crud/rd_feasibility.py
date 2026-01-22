from sqlalchemy.orm import Session
from typing import Optional
from app.models.rd_initiative import RDFeasibility
from app.schemas.rd_feasibility import RDFeasibilityCreate, RDFeasibilityUpdate


def get_feasibility(db: Session, feasibility_id: int) -> Optional[RDFeasibility]:
    """Get feasibility assessment"""
    return db.query(RDFeasibility).filter(RDFeasibility.id == feasibility_id).first()


def get_feasibility_by_initiative(db: Session, initiative_id: int) -> Optional[RDFeasibility]:
    """Get feasibility assessment for a specific initiative"""
    return db.query(RDFeasibility).filter(RDFeasibility.initiative_id == initiative_id).first()


def create_feasibility(db: Session, feasibility: RDFeasibilityCreate) -> RDFeasibility:
    """Create feasibility assessment"""
    db_feasibility = RDFeasibility(**feasibility.model_dump())
    db.add(db_feasibility)
    db.commit()
    db.refresh(db_feasibility)
    return db_feasibility


def update_feasibility(
    db: Session,
    feasibility_id: int,
    feasibility: RDFeasibilityUpdate
) -> Optional[RDFeasibility]:
    """Update feasibility assessment"""
    db_feasibility = get_feasibility(db, feasibility_id)
    if not db_feasibility:
        return None
    
    update_data = feasibility.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_feasibility, field, value)
    
    db.commit()
    db.refresh(db_feasibility)
    return db_feasibility


def delete_feasibility(db: Session, feasibility_id: int) -> bool:
    """Delete feasibility assessment"""
    db_feasibility = get_feasibility(db, feasibility_id)
    if not db_feasibility:
        return False
    
    db.delete(db_feasibility)
    db.commit()
    return True