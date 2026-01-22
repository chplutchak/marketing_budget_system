from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.rd_initiative import RDRevenue
from app.schemas.rd_revenue import RDRevenueCreate, RDRevenueUpdate


def get_revenue(db: Session, revenue_id: int) -> Optional[RDRevenue]:
    """Get a single revenue record"""
    return db.query(RDRevenue).filter(RDRevenue.id == revenue_id).first()


def get_revenue_by_initiative(db: Session, initiative_id: int) -> List[RDRevenue]:
    """Get all revenue for an initiative"""
    return db.query(RDRevenue).filter(RDRevenue.initiative_id == initiative_id).all()


def create_revenue(db: Session, revenue: RDRevenueCreate) -> RDRevenue:
    """Create a new revenue record"""
    db_revenue = RDRevenue(**revenue.model_dump())
    db.add(db_revenue)
    db.commit()
    db.refresh(db_revenue)
    return db_revenue


def update_revenue(
    db: Session,
    revenue_id: int,
    revenue: RDRevenueUpdate
) -> Optional[RDRevenue]:
    """Update revenue record"""
    db_revenue = get_revenue(db, revenue_id)
    if not db_revenue:
        return None
    
    update_data = revenue.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_revenue, field, value)
    
    db.commit()
    db.refresh(db_revenue)
    return db_revenue


def delete_revenue(db: Session, revenue_id: int) -> bool:
    """Delete revenue record"""
    db_revenue = get_revenue(db, revenue_id)
    if not db_revenue:
        return False
    
    db.delete(db_revenue)
    db.commit()
    return True


def get_total_revenue(db: Session, initiative_id: int) -> float:
    """Calculate total revenue for an initiative"""
    revenue_records = get_revenue_by_initiative(db, initiative_id)
    return sum(rev.order_value for rev in revenue_records)