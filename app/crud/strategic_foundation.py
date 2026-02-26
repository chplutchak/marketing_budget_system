from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.strategic_foundation import StrategicTarget, TargetAudience, MarketingObjective
from app.schemas.strategic_foundation import (
    StrategicTargetCreate, StrategicTargetUpdate,
    TargetAudienceCreate, TargetAudienceUpdate,
    MarketingObjectiveCreate, MarketingObjectiveUpdate
)

# ========================================
# Strategic Target CRUD
# ========================================

def get_target(db: Session, target_id: int) -> Optional[StrategicTarget]:
    return db.query(StrategicTarget).filter(StrategicTarget.id == target_id).first()

def get_targets_by_year(db: Session, year: int) -> List[StrategicTarget]:
    return db.query(StrategicTarget).filter(
        StrategicTarget.year == year
    ).order_by(StrategicTarget.order_position).all()

def create_target(db: Session, target: StrategicTargetCreate) -> StrategicTarget:
    db_target = StrategicTarget(**target.model_dump())
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target

def update_target(db: Session, target_id: int, target_update: StrategicTargetUpdate) -> Optional[StrategicTarget]:
    db_target = get_target(db, target_id)
    if not db_target:
        return None
    
    update_data = target_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_target, field, value)
    
    db.commit()
    db.refresh(db_target)
    return db_target

def delete_target(db: Session, target_id: int) -> bool:
    db_target = get_target(db, target_id)
    if not db_target:
        return False
    db.delete(db_target)
    db.commit()
    return True

# ========================================
# Target Audience CRUD
# ========================================

def get_audience(db: Session, audience_id: int) -> Optional[TargetAudience]:
    return db.query(TargetAudience).filter(TargetAudience.id == audience_id).first()

def get_audiences_by_year(db: Session, year: int) -> List[TargetAudience]:
    return db.query(TargetAudience).filter(
        TargetAudience.year == year
    ).order_by(TargetAudience.order_position).all()

def create_audience(db: Session, audience: TargetAudienceCreate) -> TargetAudience:
    db_audience = TargetAudience(**audience.model_dump())
    db.add(db_audience)
    db.commit()
    db.refresh(db_audience)
    return db_audience

def update_audience(db: Session, audience_id: int, audience_update: TargetAudienceUpdate) -> Optional[TargetAudience]:
    db_audience = get_audience(db, audience_id)
    if not db_audience:
        return None
    
    update_data = audience_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_audience, field, value)
    
    db.commit()
    db.refresh(db_audience)
    return db_audience

def delete_audience(db: Session, audience_id: int) -> bool:
    db_audience = get_audience(db, audience_id)
    if not db_audience:
        return False
    db.delete(db_audience)
    db.commit()
    return True

# ========================================
# Marketing Objective CRUD
# ========================================

def get_objective(db: Session, objective_id: int) -> Optional[MarketingObjective]:
    return db.query(MarketingObjective).filter(MarketingObjective.id == objective_id).first()

def get_objectives_by_year(db: Session, year: int) -> List[MarketingObjective]:
    return db.query(MarketingObjective).filter(
        MarketingObjective.year == year
    ).order_by(MarketingObjective.order_position).all()

def create_objective(db: Session, objective: MarketingObjectiveCreate) -> MarketingObjective:
    db_objective = MarketingObjective(**objective.model_dump())
    db.add(db_objective)
    db.commit()
    db.refresh(db_objective)
    return db_objective

def update_objective(db: Session, objective_id: int, objective_update: MarketingObjectiveUpdate) -> Optional[MarketingObjective]:
    db_objective = get_objective(db, objective_id)
    if not db_objective:
        return None
    
    update_data = objective_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_objective, field, value)
    
    db.commit()
    db.refresh(db_objective)
    return db_objective

def delete_objective(db: Session, objective_id: int) -> bool:
    db_objective = get_objective(db, objective_id)
    if not db_objective:
        return False
    db.delete(db_objective)
    db.commit()
    return True