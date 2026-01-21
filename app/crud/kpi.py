from sqlalchemy.orm import Session
from app.models.kpi import KPIMetric, KPISnapshot
from app.schemas.kpi import KPIMetricCreate, KPIMetricUpdate, KPISnapshotCreate
from typing import List, Optional
from datetime import date

# ==================== KPI METRICS ====================

def create_metric(db: Session, metric: KPIMetricCreate) -> KPIMetric:
    db_metric = KPIMetric(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

def get_all_metrics(db: Session) -> List[KPIMetric]:
    return db.query(KPIMetric).filter(KPIMetric.is_active == "active").all()

def get_metric(db: Session, metric_id: int) -> Optional[KPIMetric]:
    return db.query(KPIMetric).filter(KPIMetric.id == metric_id).first()

def update_metric(db: Session, metric_id: int, metric: KPIMetricUpdate) -> Optional[KPIMetric]:
    db_metric = get_metric(db, metric_id)
    if not db_metric:
        return None
    
    for key, value in metric.dict(exclude_unset=True).items():
        setattr(db_metric, key, value)
    
    db.commit()
    db.refresh(db_metric)
    return db_metric

def delete_metric(db: Session, metric_id: int) -> bool:
    db_metric = get_metric(db, metric_id)
    if not db_metric:
        return False
    
    db_metric.is_active = "inactive"
    db.commit()
    return True

# ==================== KPI SNAPSHOTS ====================

def create_snapshot(db: Session, snapshot: KPISnapshotCreate) -> KPISnapshot:
    db_snapshot = KPISnapshot(**snapshot.dict())
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    return db_snapshot

def get_snapshots_for_metric(
    db: Session,
    metric_id: int,
    snapshot_type: Optional[str] = None,
    limit: int = 12
) -> List[KPISnapshot]:
    query = db.query(KPISnapshot).filter(KPISnapshot.metric_id == metric_id)
    
    if snapshot_type:
        query = query.filter(KPISnapshot.snapshot_type == snapshot_type)
    
    return query.order_by(KPISnapshot.snapshot_date.desc()).limit(limit).all()

def get_latest_snapshot(
    db: Session,
    metric_id: int,
    snapshot_type: Optional[str] = None
) -> Optional[KPISnapshot]:
    query = db.query(KPISnapshot).filter(KPISnapshot.metric_id == metric_id)
    
    if snapshot_type:
        query = query.filter(KPISnapshot.snapshot_type == snapshot_type)
    
    return query.order_by(KPISnapshot.snapshot_date.desc()).first()

def delete_snapshot(db: Session, snapshot_id: int) -> bool:
    db_snapshot = db.query(KPISnapshot).filter(KPISnapshot.id == snapshot_id).first()
    if not db_snapshot:
        return False
    
    db.delete(db_snapshot)
    db.commit()
    return True

def get_snapshot_by_date(
    db: Session,
    metric_id: int,
    snapshot_date: date,
    snapshot_type: str
) -> Optional[KPISnapshot]:
    return db.query(KPISnapshot).filter(
        KPISnapshot.metric_id == metric_id,
        KPISnapshot.snapshot_date == snapshot_date,
        KPISnapshot.snapshot_type == snapshot_type
    ).first()