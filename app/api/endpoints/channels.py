from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.channels import (
    get_channel, get_channels_by_year, create_channel,
    create_multiple_channels, update_channel, delete_channel
)
from app.schemas.channels import (
    MarketingChannel, MarketingChannelCreate, MarketingChannelUpdate
)

router = APIRouter()

@router.get("/year/{year}", response_model=List[MarketingChannel])
def read_channels_by_year(year: int, db: Session = Depends(get_db)):
    return get_channels_by_year(db, year=year)

@router.get("/{channel_id}", response_model=MarketingChannel)
def read_channel(channel_id: int, db: Session = Depends(get_db)):
    channel = get_channel(db, channel_id=channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.post("/", response_model=MarketingChannel)
def create_new_channel(channel: MarketingChannelCreate, db: Session = Depends(get_db)):
    return create_channel(db=db, channel=channel)

@router.post("/bulk", response_model=List[MarketingChannel])
def create_bulk_channels(channels: List[MarketingChannelCreate], db: Session = Depends(get_db)):
    if not channels:
        raise HTTPException(status_code=400, detail="No channels provided")
    return create_multiple_channels(db=db, channels=channels)

@router.put("/{channel_id}", response_model=MarketingChannel)
def update_channel_endpoint(
    channel_id: int,
    channel_update: MarketingChannelUpdate,
    db: Session = Depends(get_db)
):
    channel = update_channel(db, channel_id=channel_id, channel_update=channel_update)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.delete("/{channel_id}")
def delete_channel_endpoint(channel_id: int, db: Session = Depends(get_db)):
    success = delete_channel(db, channel_id=channel_id)
    if not success:
        raise HTTPException(status_code=404, detail="Channel not found")
    return {"message": "Channel deleted successfully"}