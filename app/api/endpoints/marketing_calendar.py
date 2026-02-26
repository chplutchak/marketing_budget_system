from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.marketing_calendar import (
    get_calendar, get_calendar_by_month, get_calendars_by_year,
    get_all_calendars, get_calendar_with_activities,
    create_calendar, update_calendar, delete_calendar,
    get_activity, get_activities_by_calendar, get_activities_by_week,
    create_activity, create_multiple_activities, update_activity,
    toggle_activity_completion, delete_activity, delete_activities_by_week,
    get_calendar_completion_stats
)
from app.schemas.marketing_calendar import (
    MarketingCalendar, MarketingCalendarCreate, MarketingCalendarUpdate,
    MarketingActivity, MarketingActivityCreate, MarketingActivityUpdate,
    MarketingCalendarWithActivities
)

router = APIRouter()

# ========================================
# Calendar Endpoints
# ========================================

@router.get("/calendars/", response_model=List[MarketingCalendar])
def read_calendars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all calendars"""
    return get_all_calendars(db, skip=skip, limit=limit)

@router.get("/calendars/year/{year}", response_model=List[MarketingCalendar])
def read_calendars_by_year(year: int, db: Session = Depends(get_db)):
    """Get all calendars for a specific year"""
    return get_calendars_by_year(db, year=year)

@router.get("/calendars/{year}/{month}", response_model=MarketingCalendarWithActivities)
def read_calendar_with_activities(year: int, month: int, db: Session = Depends(get_db)):
    """Get calendar for a specific month with all activities"""
    calendar = get_calendar_with_activities(db, year=year, month=month)
    if not calendar:
        raise HTTPException(status_code=404, detail=f"Calendar for {year}-{month} not found")
    return calendar

@router.get("/calendars/{calendar_id}", response_model=MarketingCalendar)
def read_calendar(calendar_id: int, db: Session = Depends(get_db)):
    """Get a specific calendar by ID"""
    calendar = get_calendar(db, calendar_id=calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return calendar

@router.post("/calendars/", response_model=MarketingCalendar)
def create_new_calendar(calendar: MarketingCalendarCreate, db: Session = Depends(get_db)):
    """Create a new calendar"""
    # Check if calendar already exists for this month
    existing = get_calendar_by_month(db, year=calendar.year, month=calendar.month)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Calendar for {calendar.year}-{calendar.month} already exists"
        )
    return create_calendar(db=db, calendar=calendar)

@router.put("/calendars/{calendar_id}", response_model=MarketingCalendar)
def update_calendar_endpoint(
    calendar_id: int,
    calendar_update: MarketingCalendarUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing calendar"""
    calendar = update_calendar(db, calendar_id=calendar_id, calendar_update=calendar_update)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return calendar

@router.delete("/calendars/{calendar_id}")
def delete_calendar_endpoint(calendar_id: int, db: Session = Depends(get_db)):
    """Delete a calendar and all its activities"""
    success = delete_calendar(db, calendar_id=calendar_id)
    if not success:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return {"message": "Calendar deleted successfully"}

@router.get("/calendars/{calendar_id}/stats")
def get_calendar_stats(calendar_id: int, db: Session = Depends(get_db)):
    """Get completion statistics for a calendar"""
    calendar = get_calendar(db, calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return get_calendar_completion_stats(db, calendar_id)

# ========================================
# Activity Endpoints
# ========================================

@router.get("/activities/{activity_id}", response_model=MarketingActivity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get a specific activity by ID"""
    activity = get_activity(db, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.get("/activities/calendar/{calendar_id}", response_model=List[MarketingActivity])
def read_activities_by_calendar(calendar_id: int, db: Session = Depends(get_db)):
    """Get all activities for a calendar"""
    # Verify calendar exists
    calendar = get_calendar(db, calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return get_activities_by_calendar(db, calendar_id=calendar_id)

@router.get("/activities/calendar/{calendar_id}/week/{week_number}", response_model=List[MarketingActivity])
def read_activities_by_week(calendar_id: int, week_number: int, db: Session = Depends(get_db)):
    """Get activities for a specific week"""
    return get_activities_by_week(db, calendar_id=calendar_id, week_number=week_number)

@router.post("/activities/", response_model=MarketingActivity)
def create_new_activity(activity: MarketingActivityCreate, db: Session = Depends(get_db)):
    """Create a new activity"""
    # Verify calendar exists
    calendar = get_calendar(db, activity.calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return create_activity(db=db, activity=activity)

@router.post("/activities/bulk", response_model=List[MarketingActivity])
def create_bulk_activities(activities: List[MarketingActivityCreate], db: Session = Depends(get_db)):
    """Create multiple activities at once"""
    if not activities:
        raise HTTPException(status_code=400, detail="No activities provided")
    
    # Verify all calendars exist
    calendar_ids = set(a.calendar_id for a in activities)
    for calendar_id in calendar_ids:
        calendar = get_calendar(db, calendar_id)
        if not calendar:
            raise HTTPException(status_code=404, detail=f"Calendar {calendar_id} not found")
    
    return create_multiple_activities(db=db, activities=activities)

@router.put("/activities/{activity_id}", response_model=MarketingActivity)
def update_activity_endpoint(
    activity_id: int,
    activity_update: MarketingActivityUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing activity"""
    activity = update_activity(db, activity_id=activity_id, activity_update=activity_update)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.patch("/activities/{activity_id}/toggle", response_model=MarketingActivity)
def toggle_activity_endpoint(activity_id: int, db: Session = Depends(get_db)):
    """Toggle completion status of an activity"""
    activity = toggle_activity_completion(db, activity_id=activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.delete("/activities/{activity_id}")
def delete_activity_endpoint(activity_id: int, db: Session = Depends(get_db)):
    """Delete an activity"""
    success = delete_activity(db, activity_id=activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"}

@router.delete("/activities/calendar/{calendar_id}/week/{week_number}")
def delete_week_activities(calendar_id: int, week_number: int, db: Session = Depends(get_db)):
    """Delete all activities for a specific week"""
    count = delete_activities_by_week(db, calendar_id=calendar_id, week_number=week_number)
    return {"message": f"Deleted {count} activities"}