from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class KPIMetric(Base):
    __tablename__ = "kpi_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # "Website", "Email", "LinkedIn", "Leads", "Revenue"
    
    # Baseline and target
    baseline_value = Column(Float, nullable=True)
    baseline_label = Column(String(100), nullable=True)  # e.g., "~4,000 users/month"
    target_value = Column(Float, nullable=False)
    target_label = Column(String(100), nullable=False)  # e.g., "4,500-5,000 users/month"
    
    # Tracking info
    measurement_method = Column(String(255), nullable=False)  # e.g., "GA4 - Weekly review"
    tracking_frequency = Column(String(50), nullable=False)  # "weekly", "monthly", "both"
    unit = Column(String(50), nullable=True)  # "users", "forms", "contacts", "%", "$"
    
    # Target thresholds for color coding
    target_threshold_high = Column(Float, nullable=False, default=0.95)  # 95%+ = green
    target_threshold_low = Column(Float, nullable=False, default=0.70)   # 70%+ = yellow, <70% = red
    
    # Metadata
    is_active = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    snapshots = relationship("KPISnapshot", back_populates="metric", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<KPIMetric(name='{self.name}', target={self.target_value})>"


class KPISnapshot(Base):
    __tablename__ = "kpi_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_id = Column(Integer, ForeignKey("kpi_metrics.id"), nullable=False)
    
    # Snapshot details
    snapshot_date = Column(Date, nullable=False, index=True)
    snapshot_type = Column(String(20), nullable=False)  # "weekly" or "monthly"
    actual_value = Column(Float, nullable=False)
    
    # Optional context
    notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    metric = relationship("KPIMetric", back_populates="snapshots")
    
    def __repr__(self):
        return f"<KPISnapshot(metric_id={self.metric_id}, date={self.snapshot_date}, value={self.actual_value})>"