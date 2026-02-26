from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Dict
from app.models.marketing_calendar import MarketingCalendar, MarketingActivity
from app.schemas.marketing_calendar import (
    MarketingCalendarCreate, MarketingCalendarUpdate,
    MarketingActivityCreate, MarketingActivityUpdate
)

# ========================================
# Marketing Calendar CRUD
# ========================================

def get_calendar(db: Session, calendar_id: int) -> Optional[MarketingCalendar]:
    """Get a specific calendar by ID"""
    return db.query(MarketingCalendar).filter(MarketingCalendar.id == calendar_id).first()

def get_calendar_by_month(db: Session, year: int, month: int) -> Optional[MarketingCalendar]:
    """Get calendar for a specific year and month"""
    return db.query(MarketingCalendar).filter(
        MarketingCalendar.year == year,
        MarketingCalendar.month == month
    ).first()

def get_calendars_by_year(db: Session, year: int) -> List[MarketingCalendar]:
    """Get all calendars for a specific year"""
    return db.query(MarketingCalendar).filter(
        MarketingCalendar.year == year
    ).order_by(MarketingCalendar.month).all()

def get_all_calendars(db: Session, skip: int = 0, limit: int = 100) -> List[MarketingCalendar]:
    """Get all calendars"""
    return db.query(MarketingCalendar).order_by(
        MarketingCalendar.year.desc(),
        MarketingCalendar.month.desc()
    ).offset(skip).limit(limit).all()

def get_calendar_with_activities(db: Session, year: int, month: int) -> Optional[MarketingCalendar]:
    """Get calendar with all its activities"""
    return db.query(MarketingCalendar).options(
        joinedload(MarketingCalendar.activities)
    ).filter(
        MarketingCalendar.year == year,
        MarketingCalendar.month == month
    ).first()

def create_calendar(db: Session, calendar: MarketingCalendarCreate) -> MarketingCalendar:
    """Create a new calendar"""
    db_calendar = MarketingCalendar(**calendar.model_dump())
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar

def update_calendar(db: Session, calendar_id: int, calendar_update: MarketingCalendarUpdate) -> Optional[MarketingCalendar]:
    """Update an existing calendar"""
    db_calendar = get_calendar(db, calendar_id)
    if not db_calendar:
        return None
    
    update_data = calendar_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_calendar, field, value)
    
    db.commit()
    db.refresh(db_calendar)
    return db_calendar

def delete_calendar(db: Session, calendar_id: int) -> bool:
    """Delete a calendar and all its activities"""
    db_calendar = get_calendar(db, calendar_id)
    if not db_calendar:
        return False
    
    db.delete(db_calendar)
    db.commit()
    return True

# ========================================
# Marketing Activity CRUD
# ========================================

def get_activity(db: Session, activity_id: int) -> Optional[MarketingActivity]:
    """Get a specific activity by ID"""
    return db.query(MarketingActivity).filter(MarketingActivity.id == activity_id).first()

def get_activities_by_calendar(db: Session, calendar_id: int) -> List[MarketingActivity]:
    """Get all activities for a calendar"""
    return db.query(MarketingActivity).filter(
        MarketingActivity.calendar_id == calendar_id
    ).order_by(
        MarketingActivity.week_number,
        MarketingActivity.order_in_week
    ).all()

def get_activities_by_week(db: Session, calendar_id: int, week_number: int) -> List[MarketingActivity]:
    """Get activities for a specific week"""
    return db.query(MarketingActivity).filter(
        MarketingActivity.calendar_id == calendar_id,
        MarketingActivity.week_number == week_number
    ).order_by(MarketingActivity.order_in_week).all()

def create_activity(db: Session, activity: MarketingActivityCreate) -> MarketingActivity:
    """Create a new activity"""
    db_activity = MarketingActivity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def create_multiple_activities(db: Session, activities: List[MarketingActivityCreate]) -> List[MarketingActivity]:
    """Create multiple activities at once"""
    db_activities = [MarketingActivity(**activity.model_dump()) for activity in activities]
    db.add_all(db_activities)
    db.commit()
    for activity in db_activities:
        db.refresh(activity)
    return db_activities

def update_activity(db: Session, activity_id: int, activity_update: MarketingActivityUpdate) -> Optional[MarketingActivity]:
    """Update an existing activity"""
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return None
    
    update_data = activity_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_activity, field, value)
    
    db.commit()
    db.refresh(db_activity)
    return db_activity

def toggle_activity_completion(db: Session, activity_id: int) -> Optional[MarketingActivity]:
    """Toggle completion status of an activity"""
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return None
    
    db_activity.is_completed = not db_activity.is_completed
    db.commit()
    db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int) -> bool:
    """Delete an activity"""
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return False
    
    db.delete(db_activity)
    db.commit()
    return True

def delete_activities_by_week(db: Session, calendar_id: int, week_number: int) -> int:
    """Delete all activities for a specific week"""
    count = db.query(MarketingActivity).filter(
        MarketingActivity.calendar_id == calendar_id,
        MarketingActivity.week_number == week_number
    ).delete()
    db.commit()
    return count

# ========================================
# Utility Functions
# ========================================

def get_calendar_completion_stats(db: Session, calendar_id: int) -> Dict:
    """Get completion statistics for a calendar"""
    activities = get_activities_by_calendar(db, calendar_id)
    
    total = len(activities)
    completed = sum(1 for a in activities if a.is_completed)
    
    return {
        "total_activities": total,
        "completed_activities": completed,
        "pending_activities": total - completed,
        "completion_percentage": round((completed / total * 100), 2) if total > 0 else 0
    }