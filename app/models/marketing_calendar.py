from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class MarketingCalendar(Base):
    """Monthly marketing calendar entries"""
    __tablename__ = "marketing_calendars"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)  # 1-12
    focus = Column(String(255), nullable=True)
    major_campaigns = Column(JSON, nullable=True)  # ["Campaign 1", "Campaign 2"]
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activities = relationship("MarketingActivity", back_populates="calendar", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MarketingCalendar(year={self.year}, month={self.month})>"


class MarketingActivity(Base):
    """Individual marketing activities within a calendar month"""
    __tablename__ = "marketing_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    calendar_id = Column(Integer, ForeignKey("marketing_calendars.id"), nullable=False)
    
    # Activity details
    week_number = Column(Integer, nullable=False)  # 1-4
    activity_name = Column(String(500), nullable=False)
    day_of_week = Column(String(20), nullable=False)  # monday, tuesday, etc.
    order_in_week = Column(Integer, default=0)  # For ordering within a week
    
    # Completion tracking
    is_completed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    calendar = relationship("MarketingCalendar", back_populates="activities")
    
    def __repr__(self):
        return f"<MarketingActivity(week={self.week_number}, activity='{self.activity_name}')>"