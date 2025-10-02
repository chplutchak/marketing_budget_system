from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ROIMetric(Base):
    __tablename__ = "roi_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    
    # ROI calculation period
    calculation_date = Column(Date, nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Financial metrics
    total_cost = Column(Float, nullable=False, default=0.0)
    revenue_attributed = Column(Float, nullable=False, default=0.0)
    roi_percentage = Column(Float, nullable=True)  # Calculated: (revenue - cost) / cost * 100
    
    # Performance metrics (stored as JSON for flexibility)
    performance_metrics = Column(JSON, nullable=True)  # e.g., {"leads": 150, "conversions": 25, "cpa": 120}
    
    # Attribution details
    attribution_method = Column(String(50), default="last_touch")  # last_touch, first_touch, linear, etc.
    attribution_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    campaign = relationship("Campaign")
    
    def __repr__(self):
        return f"<ROIMetric(campaign_id={self.campaign_id}, roi={self.roi_percentage}%)>"