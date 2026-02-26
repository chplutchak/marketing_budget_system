from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class StrategicTarget(Base):
    """2026 Strategic Targets/Metrics"""
    __tablename__ = "strategic_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    
    # Target details
    metric_name = Column(String(255), nullable=False)
    target_value = Column(String(100), nullable=False)
    delta_value = Column(String(100), nullable=True)
    order_position = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<StrategicTarget(metric='{self.metric_name}')>"


class TargetAudience(Base):
    """Target audience segments"""
    __tablename__ = "target_audiences"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    
    # Audience details
    priority = Column(String(50), nullable=False)  # "PRIMARY", "SECONDARY", etc.
    audience_name = Column(String(255), nullable=False)
    color = Column(String(20), nullable=True)  # Hex color
    icon = Column(String(10), nullable=True)  # Emoji
    
    # Details (JSON)
    # {"Examples": "...", "Cycle": "...", "Strategy": "...", "Count": "...", "Value": "..."}
    details = Column(JSON, nullable=True)
    
    order_position = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<TargetAudience(name='{self.audience_name}', priority='{self.priority}')>"


class MarketingObjective(Base):
    """Marketing objectives/goals"""
    __tablename__ = "marketing_objectives"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    
    # Objective details
    icon = Column(String(10), nullable=True)
    title = Column(String(255), nullable=False)
    target = Column(String(500), nullable=False)
    measurement = Column(String(255), nullable=False)
    order_position = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<MarketingObjective(title='{self.title}')>"