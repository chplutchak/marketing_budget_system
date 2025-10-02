from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.crud.roi import (
    get_roi_metric, get_roi_metrics, get_roi_metrics_by_campaign,
    get_roi_metrics_by_date_range, get_roi_metrics_with_campaign,
    create_roi_metric, update_roi_metric, delete_roi_metric,
    get_campaign_roi_summary
)
from app.schemas.roi import ROIMetric, ROIMetricCreate, ROIMetricUpdate

router = APIRouter()

@router.get("/", response_model=List[ROIMetric])
def read_roi_metrics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all ROI metrics"""
    return get_roi_metrics(db, skip=skip, limit=limit)

@router.get("/with-campaign")
def read_roi_metrics_with_campaign(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get ROI metrics with campaign names"""
    results = get_roi_metrics_with_campaign(db, skip=skip, limit=limit)
    
    metrics = []
    for roi, campaign_name in results:
        metric_dict = {
            "id": roi.id,
            "campaign_id": roi.campaign_id,
            "calculation_date": roi.calculation_date,
            "period_start": roi.period_start,
            "period_end": roi.period_end,
            "total_cost": roi.total_cost,
            "revenue_attributed": roi.revenue_attributed,
            "roi_percentage": roi.roi_percentage,
            "performance_metrics": roi.performance_metrics,
            "attribution_method": roi.attribution_method,
            "attribution_notes": roi.attribution_notes,
            "created_at": roi.created_at,
            "updated_at": roi.updated_at,
            "campaign_name": campaign_name
        }
        metrics.append(metric_dict)
    
    return metrics

@router.get("/campaign/{campaign_id}", response_model=List[ROIMetric])
def read_roi_metrics_by_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get all ROI metrics for a specific campaign"""
    return get_roi_metrics_by_campaign(db, campaign_id=campaign_id)

@router.get("/date-range")
def read_roi_metrics_by_date_range(
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db)
):
    """Get ROI metrics within a date range"""
    return get_roi_metrics_by_date_range(db, start_date=start_date, end_date=end_date)

@router.get("/summary/campaign/{campaign_id}")
def get_roi_summary(campaign_id: int, db: Session = Depends(get_db)):
    """Get ROI summary for a campaign"""
    return get_campaign_roi_summary(db, campaign_id=campaign_id)

@router.get("/{roi_id}", response_model=ROIMetric)
def read_roi_metric(roi_id: int, db: Session = Depends(get_db)):
    """Get a specific ROI metric by ID"""
    roi = get_roi_metric(db, roi_id=roi_id)
    if roi is None:
        raise HTTPException(status_code=404, detail="ROI metric not found")
    return roi

@router.post("/", response_model=ROIMetric)
def create_new_roi_metric(roi: ROIMetricCreate, db: Session = Depends(get_db)):
    """Create a new ROI metric"""
    # Verify campaign exists
    from app.crud.campaign import get_campaign
    campaign = get_campaign(db, roi.campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return create_roi_metric(db=db, roi=roi)

@router.put("/{roi_id}", response_model=ROIMetric)
def update_roi_metric_endpoint(roi_id: int, roi_update: ROIMetricUpdate, db: Session = Depends(get_db)):
    """Update an existing ROI metric"""
    roi = update_roi_metric(db, roi_id=roi_id, roi_update=roi_update)
    if roi is None:
        raise HTTPException(status_code=404, detail="ROI metric not found")
    return roi

@router.delete("/{roi_id}")
def delete_roi_metric_endpoint(roi_id: int, db: Session = Depends(get_db)):
    """Delete an ROI metric"""
    success = delete_roi_metric(db, roi_id=roi_id)
    if not success:
        raise HTTPException(status_code=404, detail="ROI metric not found")
    return {"message": "ROI metric deleted successfully"}