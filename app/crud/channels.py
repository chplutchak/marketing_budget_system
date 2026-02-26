from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.channels import MarketingChannel
from app.schemas.channels import MarketingChannelCreate, MarketingChannelUpdate

def get_channel(db: Session, channel_id: int) -> Optional[MarketingChannel]:
    return db.query(MarketingChannel).filter(MarketingChannel.id == channel_id).first()

def get_channels_by_year(db: Session, year: int) -> List[MarketingChannel]:
    return db.query(MarketingChannel).filter(
        MarketingChannel.year == year
    ).order_by(MarketingChannel.order_position).all()

def create_channel(db: Session, channel: MarketingChannelCreate) -> MarketingChannel:
    db_channel = MarketingChannel(**channel.model_dump())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def create_multiple_channels(db: Session, channels: List[MarketingChannelCreate]) -> List[MarketingChannel]:
    db_channels = [MarketingChannel(**channel.model_dump()) for channel in channels]
    db.add_all(db_channels)
    db.commit()
    for channel in db_channels:
        db.refresh(channel)
    return db_channels

def update_channel(db: Session, channel_id: int, channel_update: MarketingChannelUpdate) -> Optional[MarketingChannel]:
    db_channel = get_channel(db, channel_id)
    if not db_channel:
        return None
    
    update_data = channel_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_channel, field, value)
    
    db.commit()
    db.refresh(db_channel)
    return db_channel

def delete_channel(db: Session, channel_id: int) -> bool:
    db_channel = get_channel(db, channel_id)
    if not db_channel:
        return False
    db.delete(db_channel)
    db.commit()
    return True