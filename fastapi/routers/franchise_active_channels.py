from fastapi import APIRouter, Depends, HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from schemas import FranchiseActiveChannelCreate, FranchiseActiveChannelUpdate  # type: ignore
from services.franchise_active_channel_service import FranchiseActiveChannelService  # type: ignore

router = APIRouter(prefix="/franchise_active_channels", tags=["FranchiseActiveChannels"])

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    try:
        data = FranchiseActiveChannelService.get_all(db)
        return {"status": "success", "data": [dict(row) for row in data]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        data = FranchiseActiveChannelService.get_by_id(db, id)
        if not data:
            raise HTTPException(status_code=404, detail="Not found")
        return {"status": "success", "data": dict(data)}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/")
def create(entity: FranchiseActiveChannelCreate, db: Session = Depends(get_db)):
    try:
        new_id = FranchiseActiveChannelService.create(db, entity)
        return {"status": "success", "message": "Created successfully", "id": new_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.put("/{id}")
@router.patch("/{id}")
def update(id: int, entity: FranchiseActiveChannelUpdate, db: Session = Depends(get_db)):
    try:
        updated = FranchiseActiveChannelService.update(db, id, entity)
        if not updated:
            raise HTTPException(status_code=404, detail="Not found or no fields to update")
        return {"status": "success", "message": "Updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
