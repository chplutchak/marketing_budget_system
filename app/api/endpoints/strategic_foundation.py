from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.strategic_foundation import (
    get_target, get_targets_by_year, create_target, update_target, delete_target,
    get_audience, get_audiences_by_year, create_audience, update_audience, delete_audience,
    get_objective, get_objectives_by_year, create_objective, update_objective, delete_objective
)
from app.schemas.strategic_foundation import (
    StrategicTarget, StrategicTargetCreate, StrategicTargetUpdate,
    TargetAudience, TargetAudienceCreate, TargetAudienceUpdate,
    MarketingObjective, MarketingObjectiveCreate, MarketingObjectiveUpdate
)

router = APIRouter()

# ========================================
# Strategic Target Endpoints
# ========================================

@router.get("/targets/year/{year}", response_model=List[StrategicTarget])
def read_targets_by_year(year: int, db: Session = Depends(get_db)):
    return get_targets_by_year(db, year=year)

@router.get("/targets/{target_id}", response_model=StrategicTarget)
def read_target(target_id: int, db: Session = Depends(get_db)):
    target = get_target(db, target_id=target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target

@router.post("/targets/", response_model=StrategicTarget)
def create_new_target(target: StrategicTargetCreate, db: Session = Depends(get_db)):
    return create_target(db=db, target=target)

@router.put("/targets/{target_id}", response_model=StrategicTarget)
def update_target_endpoint(
    target_id: int,
    target_update: StrategicTargetUpdate,
    db: Session = Depends(get_db)
):
    target = update_target(db, target_id=target_id, target_update=target_update)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target

@router.delete("/targets/{target_id}")
def delete_target_endpoint(target_id: int, db: Session = Depends(get_db)):
    success = delete_target(db, target_id=target_id)
    if not success:
        raise HTTPException(status_code=404, detail="Target not found")
    return {"message": "Target deleted successfully"}

# ========================================
# Target Audience Endpoints
# ========================================

@router.get("/audiences/year/{year}", response_model=List[TargetAudience])
def read_audiences_by_year(year: int, db: Session = Depends(get_db)):
    return get_audiences_by_year(db, year=year)

@router.get("/audiences/{audience_id}", response_model=TargetAudience)
def read_audience(audience_id: int, db: Session = Depends(get_db)):
    audience = get_audience(db, audience_id=audience_id)
    if not audience:
        raise HTTPException(status_code=404, detail="Audience not found")
    return audience

@router.post("/audiences/", response_model=TargetAudience)
def create_new_audience(audience: TargetAudienceCreate, db: Session = Depends(get_db)):
    return create_audience(db=db, audience=audience)

@router.put("/audiences/{audience_id}", response_model=TargetAudience)
def update_audience_endpoint(
    audience_id: int,
    audience_update: TargetAudienceUpdate,
    db: Session = Depends(get_db)
):
    audience = update_audience(db, audience_id=audience_id, audience_update=audience_update)
    if not audience:
        raise HTTPException(status_code=404, detail="Audience not found")
    return audience

@router.delete("/audiences/{audience_id}")
def delete_audience_endpoint(audience_id: int, db: Session = Depends(get_db)):
    success = delete_audience(db, audience_id=audience_id)
    if not success:
        raise HTTPException(status_code=404, detail="Audience not found")
    return {"message": "Audience deleted successfully"}

# ========================================
# Marketing Objective Endpoints
# ========================================

@router.get("/objectives/year/{year}", response_model=List[MarketingObjective])
def read_objectives_by_year(year: int, db: Session = Depends(get_db)):
    return get_objectives_by_year(db, year=year)

@router.get("/objectives/{objective_id}", response_model=MarketingObjective)
def read_objective(objective_id: int, db: Session = Depends(get_db)):
    objective = get_objective(db, objective_id=objective_id)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")
    return objective

@router.post("/objectives/", response_model=MarketingObjective)
def create_new_objective(objective: MarketingObjectiveCreate, db: Session = Depends(get_db)):
    return create_objective(db=db, objective=objective)

@router.put("/objectives/{objective_id}", response_model=MarketingObjective)
def update_objective_endpoint(
    objective_id: int,
    objective_update: MarketingObjectiveUpdate,
    db: Session = Depends(get_db)
):
    objective = update_objective(db, objective_id=objective_id, objective_update=objective_update)
    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")
    return objective

@router.delete("/objectives/{objective_id}")
def delete_objective_endpoint(objective_id: int, db: Session = Depends(get_db)):
    success = delete_objective(db, objective_id=objective_id)
    if not success:
        raise HTTPException(status_code=404, detail="Objective not found")
    return {"message": "Objective deleted successfully"}