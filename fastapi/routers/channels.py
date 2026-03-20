from fastapi import APIRouter, Depends, HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from schemas import ChannelCreate, ChannelUpdate  # type: ignore
from services.channel_service import ChannelService  # type: ignore

router = APIRouter(prefix="/channels", tags=["Channels"])

@router.get("/")
def get_channels(db: Session = Depends(get_db)):
    try:
        data = ChannelService.get_all(db)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{channel_id}")
def get_channel(channel_id: int, db: Session = Depends(get_db)):
    try:
        data = ChannelService.get_by_id(db, channel_id)
        if not data:
            raise HTTPException(status_code=404, detail="Channel not found")
        return {"status": "success", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/")
def create_channel(channel: ChannelCreate, db: Session = Depends(get_db)):
    try:
        channel_id = ChannelService.create(db, channel)
        return {"status": "success", "message": "Channel created successfully", "id": channel_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.put("/{channel_id}")
@router.patch("/{channel_id}")
def update_channel(channel_id: int, channel: ChannelUpdate, db: Session = Depends(get_db)):
    try:
        updated = ChannelService.update(db, channel_id, channel)
        if not updated:
            raise HTTPException(status_code=404, detail="Channel not found or no fields to update")
        return {"status": "success", "message": "Channel updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
