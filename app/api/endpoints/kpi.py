from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
from app import crud
from app.database import get_db
from app.schemas.kpi import (
    KPIMetricCreate, KPIMetricUpdate, KPIMetricResponse,
    KPISnapshotCreate, KPISnapshotResponse
)

router = APIRouter()

# ==================== KPI METRICS ====================

@router.post("/metrics/", response_model=KPIMetricResponse)
def create_kpi_metric(metric: KPIMetricCreate, db: Session = Depends(get_db)):
    return crud.kpi.create_metric(db, metric)

@router.get("/metrics/", response_model=List[KPIMetricResponse])
def get_all_metrics(db: Session = Depends(get_db)):
    return crud.kpi.get_all_metrics(db)

@router.get("/metrics/{metric_id}", response_model=KPIMetricResponse)
def get_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = crud.kpi.get_metric(db, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@router.put("/metrics/{metric_id}", response_model=KPIMetricResponse)
def update_metric(metric_id: int, metric: KPIMetricUpdate, db: Session = Depends(get_db)):
    updated = crud.kpi.update_metric(db, metric_id, metric)
    if not updated:
        raise HTTPException(status_code=404, detail="Metric not found")
    return updated

@router.delete("/metrics/{metric_id}")
def delete_metric(metric_id: int, db: Session = Depends(get_db)):
    success = crud.kpi.delete_metric(db, metric_id)
    if not success:
        raise HTTPException(status_code=404, detail="Metric not found")
    return {"success": True}

# ==================== KPI SNAPSHOTS ====================

@router.post("/snapshots/", response_model=KPISnapshotResponse)
def create_snapshot(snapshot: KPISnapshotCreate, db: Session = Depends(get_db)):
    return crud.kpi.create_snapshot(db, snapshot)

@router.get("/snapshots/metric/{metric_id}", response_model=List[KPISnapshotResponse])
def get_snapshots_for_metric(
    metric_id: int,
    snapshot_type: str = None,  # "weekly" or "monthly"
    limit: int = 12,
    db: Session = Depends(get_db)
):
    return crud.kpi.get_snapshots_for_metric(db, metric_id, snapshot_type, limit)

@router.get("/snapshots/latest/{metric_id}")
def get_latest_snapshot(metric_id: int, snapshot_type: str = None, db: Session = Depends(get_db)):
    snapshot = crud.kpi.get_latest_snapshot(db, metric_id, snapshot_type)
    if not snapshot:
        return None
    return snapshot

@router.delete("/snapshots/{snapshot_id}")
def delete_snapshot(snapshot_id: int, db: Session = Depends(get_db)):
    success = crud.kpi.delete_snapshot(db, snapshot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return {"success": True}

# ==================== DASHBOARD DATA ====================

@router.get("/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get summary data for all metrics with latest snapshots"""
    metrics = crud.kpi.get_all_metrics(db)
    
    summary = []
    for metric in metrics:
        weekly_snapshot = crud.kpi.get_latest_snapshot(db, metric.id, "weekly")
        monthly_snapshot = crud.kpi.get_latest_snapshot(db, metric.id, "monthly")
        
        summary.append({
            "metric": metric,
            "latest_weekly": weekly_snapshot,
            "latest_monthly": monthly_snapshot,
            "weekly_history": crud.kpi.get_snapshots_for_metric(db, metric.id, "weekly", 12),
            "monthly_history": crud.kpi.get_snapshots_for_metric(db, metric.id, "monthly", 12)
        })
    
    return summary