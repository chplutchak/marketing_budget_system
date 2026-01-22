from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.rd_initiative import RDSample
from app.schemas.rd_sample import RDSampleCreate, RDSampleUpdate


def get_sample(db: Session, sample_id: int) -> Optional[RDSample]:
    """Get a single sample record"""
    return db.query(RDSample).filter(RDSample.id == sample_id).first()


def get_samples_by_initiative(db: Session, initiative_id: int) -> List[RDSample]:
    """Get all samples for an initiative"""
    return db.query(RDSample).filter(RDSample.initiative_id == initiative_id).all()


def create_sample(db: Session, sample: RDSampleCreate) -> RDSample:
    """Create a new sample record"""
    db_sample = RDSample(**sample.model_dump())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample


def update_sample(
    db: Session,
    sample_id: int,
    sample: RDSampleUpdate
) -> Optional[RDSample]:
    """Update sample record"""
    db_sample = get_sample(db, sample_id)
    if not db_sample:
        return None
    
    update_data = sample.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sample, field, value)
    
    db.commit()
    db.refresh(db_sample)
    return db_sample


def delete_sample(db: Session, sample_id: int) -> bool:
    """Delete sample record"""
    db_sample = get_sample(db, sample_id)
    if not db_sample:
        return False
    
    db.delete(db_sample)
    db.commit()
    return True


def get_converted_samples(db: Session, initiative_id: int) -> List[RDSample]:
    """Get samples that resulted in orders for an initiative"""
    return db.query(RDSample).filter(
        RDSample.initiative_id == initiative_id,
        RDSample.converted_to_order == "yes"
    ).all()