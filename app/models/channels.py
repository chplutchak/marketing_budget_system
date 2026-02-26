from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class MarketingChannel(Base):
    """Marketing channel execution plans"""
    __tablename__ = "marketing_channels"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    
    # Channel details
    channel_name = Column(String(255), nullable=False)
    icon = Column(String(10), nullable=True)
    color = Column(String(20), nullable=True)  # Hex color
    
    frequency = Column(String(100), nullable=False)
    days = Column(String(255), nullable=False)
    time_commitment = Column(String(100), nullable=False)
    budget = Column(String(100), nullable=False)
    
    # Tactics (JSON array)
    # ["Tactic 1", "Tactic 2", ...]
    tactics = Column(JSON, nullable=True)
    
    order_position = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<MarketingChannel(name='{self.channel_name}')>"