from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.rd_initiative import RDCustomerInterest
from app.schemas.rd_customer_interest import RDCustomerInterestCreate, RDCustomerInterestUpdate


def get_customer_interest(db: Session, interest_id: int) -> Optional[RDCustomerInterest]:
    """Get a single customer interest record"""
    return db.query(RDCustomerInterest).filter(RDCustomerInterest.id == interest_id).first()


def get_customers_by_initiative(
    db: Session, 
    initiative_id: int,
    interest_level: Optional[str] = None
) -> List[RDCustomerInterest]:
    """Get all customer interest records for an initiative"""
    query = db.query(RDCustomerInterest).filter(RDCustomerInterest.initiative_id == initiative_id)
    
    if interest_level:
        query = query.filter(RDCustomerInterest.interest_level == interest_level)
    
    return query.all()


def create_customer_interest(db: Session, interest: RDCustomerInterestCreate) -> RDCustomerInterest:
    """Create a new customer interest record"""
    db_interest = RDCustomerInterest(**interest.model_dump())
    db.add(db_interest)
    db.commit()
    db.refresh(db_interest)
    return db_interest


def update_customer_interest(
    db: Session,
    interest_id: int,
    interest: RDCustomerInterestUpdate
) -> Optional[RDCustomerInterest]:
    """Update customer interest record"""
    db_interest = get_customer_interest(db, interest_id)
    if not db_interest:
        return None
    
    update_data = interest.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_interest, field, value)
    
    db.commit()
    db.refresh(db_interest)
    return db_interest


def delete_customer_interest(db: Session, interest_id: int) -> bool:
    """Delete customer interest record"""
    db_interest = get_customer_interest(db, interest_id)
    if not db_interest:
        return False
    
    db.delete(db_interest)
    db.commit()
    return True