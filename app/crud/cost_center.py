from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.cost_center import CostCenter
from app.schemas.cost_center import CostCenterCreate, CostCenterUpdate

def get_cost_center(db: Session, cost_center_id: int) -> Optional[CostCenter]:
    return db.query(CostCenter).filter(CostCenter.id == cost_center_id).first()

def get_cost_center_by_code(db: Session, code: str) -> Optional[CostCenter]:
    return db.query(CostCenter).filter(CostCenter.code == code).first()

def get_cost_centers(db: Session, skip: int = 0, limit: int = 100) -> List[CostCenter]:
    return db.query(CostCenter).offset(skip).limit(limit).all()

def get_active_cost_centers(db: Session) -> List[CostCenter]:
    return db.query(CostCenter).filter(CostCenter.is_active == True).all()

def get_cost_centers_by_department(db: Session, department: str) -> List[CostCenter]:
    return db.query(CostCenter).filter(CostCenter.department == department).all()

def create_cost_center(db: Session, cost_center: CostCenterCreate) -> CostCenter:
    db_cost_center = CostCenter(**cost_center.dict())
    db.add(db_cost_center)
    db.commit()
    db.refresh(db_cost_center)
    return db_cost_center

def update_cost_center(db: Session, cost_center_id: int, cost_center_update: CostCenterUpdate) -> Optional[CostCenter]:
    db_cost_center = db.query(CostCenter).filter(CostCenter.id == cost_center_id).first()
    if db_cost_center:
        update_data = cost_center_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cost_center, field, value)
        db.commit()
        db.refresh(db_cost_center)
    return db_cost_center

def delete_cost_center(db: Session, cost_center_id: int) -> bool:
    db_cost_center = db.query(CostCenter).filter(CostCenter.id == cost_center_id).first()
    if db_cost_center:
        # Don't actually delete, just deactivate to preserve data integrity
        db_cost_center.is_active = False
        db.commit()
        return True
    return False