from fastapi import APIRouter, Depends, HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from schemas import FranchiseCreate, FranchiseUpdate  # type: ignore
from services.franchise_service import FranchiseService  # type: ignore

router = APIRouter(prefix="/franchises", tags=["Franchises"])

@router.get("/")
def get_franchises(db: Session = Depends(get_db)):
    try:
        data = FranchiseService.get_all(db)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/")
def create_franchise(franchise: FranchiseCreate, db: Session = Depends(get_db)):
    try:
        franchise_id = FranchiseService.create(db, franchise)
        return {"status": "success", "message": "Franchise created successfully", "id": franchise_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.put("/{franchise_id}")
@router.patch("/{franchise_id}")
def update_franchise(franchise_id: int, franchise: FranchiseUpdate, db: Session = Depends(get_db)):
    try:
        updated = FranchiseService.update(db, franchise_id, franchise)
        if not updated:
            raise HTTPException(status_code=404, detail="Franchise not found or no fields to update")
        return {"status": "success", "message": "Franchise updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
