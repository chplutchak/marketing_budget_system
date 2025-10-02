from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.models.roi import ROIMetric
from app.models.campaign import Campaign
from app.schemas.roi import ROIMetricCreate, ROIMetricUpdate

def calculate_roi_percentage(revenue: float, cost: float) -> float:
    if cost == 0:
        return 0.0
    return ((revenue - cost) / cost) * 100

def get_roi_metric(db: Session, roi_id: int) -> Optional[ROIMetric]:
    return db.query(ROIMetric).filter(ROIMetric.id == roi_id).first()

def get_roi_metrics(db: Session, skip: int = 0, limit: int = 100) -> List[ROIMetric]:
    return db.query(ROIMetric).offset(skip).limit(limit).all()

def get_roi_metrics_by_campaign(db: Session, campaign_id: int) -> List[ROIMetric]:
    return db.query(ROIMetric).filter(ROIMetric.campaign_id == campaign_id).all()

def get_roi_metrics_by_date_range(db: Session, start_date: date, end_date: date) -> List[ROIMetric]:
    return db.query(ROIMetric).filter(
        ROIMetric.period_start >= start_date,
        ROIMetric.period_end <= end_date
    ).all()

def get_roi_metrics_with_campaign(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(
            ROIMetric,
            Campaign.name.label('campaign_name')
        )
        .join(Campaign, ROIMetric.campaign_id == Campaign.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_roi_metric(db: Session, roi: ROIMetricCreate) -> ROIMetric:
    roi_percentage = calculate_roi_percentage(roi.revenue_attributed, roi.total_cost)
    
    performance_json = None
    if roi.performance_metrics:
        performance_json = {str(k): float(v) for k, v in roi.performance_metrics.items()}
    
    db_roi = ROIMetric(
        campaign_id=roi.campaign_id,
        calculation_date=roi.calculation_date,
        period_start=roi.period_start,
        period_end=roi.period_end,
        total_cost=roi.total_cost,
        revenue_attributed=roi.revenue_attributed,
        roi_percentage=roi_percentage,
        performance_metrics=performance_json,
        attribution_method=roi.attribution_method,
        attribution_notes=roi.attribution_notes
    )
    
    db.add(db_roi)
    db.commit()
    db.refresh(db_roi)
    return db_roi

def update_roi_metric(db: Session, roi_id: int, roi_update: ROIMetricUpdate) -> Optional[ROIMetric]:
    db_roi = db.query(ROIMetric).filter(ROIMetric.id == roi_id).first()
    if db_roi:
        update_data = roi_update.dict(exclude_unset=True)
        
        if 'performance_metrics' in update_data and update_data['performance_metrics']:
            update_data['performance_metrics'] = {str(k): float(v) for k, v in update_data['performance_metrics'].items()}
        
        for field, value in update_data.items():
            setattr(db_roi, field, value)
        
        if 'total_cost' in update_data or 'revenue_attributed' in update_data:
            db_roi.roi_percentage = calculate_roi_percentage(db_roi.revenue_attributed, db_roi.total_cost)
        
        db.commit()
        db.refresh(db_roi)
    return db_roi

def delete_roi_metric(db: Session, roi_id: int) -> bool:
    db_roi = db.query(ROIMetric).filter(ROIMetric.id == roi_id).first()
    if db_roi:
        db.delete(db_roi)
        db.commit()
        return True
    return False

def get_campaign_roi_summary(db: Session, campaign_id: int):
    roi_metrics = get_roi_metrics_by_campaign(db, campaign_id)
    
    if not roi_metrics:
        return {
            "campaign_id": campaign_id,
            "total_cost": 0.0,
            "total_revenue": 0.0,
            "overall_roi": 0.0,
            "metric_count": 0
        }
    
    total_cost = sum(m.total_cost for m in roi_metrics)
    total_revenue = sum(m.revenue_attributed for m in roi_metrics)
    overall_roi = calculate_roi_percentage(total_revenue, total_cost)
    
    return {
        "campaign_id": campaign_id,
        "total_cost": total_cost,
        "total_revenue": total_revenue,
        "overall_roi": overall_roi,
        "metric_count": len(roi_metrics)
    }