from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.rd_initiative import RDContact
from app.schemas.rd_contact import RDContactCreate, RDContactUpdate


def get_contact(db: Session, contact_id: int) -> Optional[RDContact]:
    """Get a single contact record"""
    return db.query(RDContact).filter(RDContact.id == contact_id).first()


def get_contacts_by_initiative(
    db: Session,
    initiative_id: int,
    contact_type: Optional[str] = None,
    department: Optional[str] = None
) -> List[RDContact]:
    """Get all contact records for an initiative"""
    query = db.query(RDContact).filter(RDContact.initiative_id == initiative_id)
    
    if contact_type:
        query = query.filter(RDContact.contact_type == contact_type)
    if department:
        query = query.filter(RDContact.department == department)
    
    return query.order_by(RDContact.contact_date.desc()).all()


def create_contact(db: Session, contact: RDContactCreate) -> RDContact:
    """Create a new contact record"""
    db_contact = RDContact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(
    db: Session,
    contact_id: int,
    contact: RDContactUpdate
) -> Optional[RDContact]:
    """Update contact record"""
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None
    
    update_data = contact.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_contact, field, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int) -> bool:
    """Delete contact record"""
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return False
    
    db.delete(db_contact)
    db.commit()
    return True