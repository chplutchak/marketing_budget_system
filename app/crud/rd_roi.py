from sqlalchemy.orm import Session
from typing import Optional
from app.models.rd_initiative import RDROI
from app.schemas.rd_roi import RDROICreate, RDROIUpdate


def get_roi(db: Session, roi_id: int) -> Optional[RDROI]:
    """Get ROI record"""
    return db.query(RDROI).filter(RDROI.id == roi_id).first()


def get_roi_by_initiative(db: Session, initiative_id: int) -> Optional[RDROI]:
    """Get ROI data for a specific initiative"""
    return db.query(RDROI).filter(RDROI.initiative_id == initiative_id).first()


def create_roi(db: Session, roi: RDROICreate) -> RDROI:
    """Create ROI record"""
    db_roi = RDROI(**roi.model_dump())
    db.add(db_roi)
    db.commit()
    db.refresh(db_roi)
    return db_roi


def update_roi(
    db: Session,
    roi_id: int,
    roi: RDROIUpdate
) -> Optional[RDROI]:
    """Update ROI record"""
    db_roi = get_roi(db, roi_id)
    if not db_roi:
        return None
    
    update_data = roi.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_roi, field, value)
    
    db.commit()
    db.refresh(db_roi)
    return db_roi


def delete_roi(db: Session, roi_id: int) -> bool:
    """Delete ROI record"""
    db_roi = get_roi(db, roi_id)
    if not db_roi:
        return False
    
    db.delete(db_roi)
    db.commit()
    return True