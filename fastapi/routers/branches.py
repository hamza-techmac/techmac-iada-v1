from fastapi import APIRouter, Depends, HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from schemas import BranchCreate, BranchUpdate  # type: ignore
from services.branch_service import BranchService  # type: ignore

router = APIRouter(prefix="/branches", tags=["Branches"])

@router.get("/")
def get_branches(db: Session = Depends(get_db)):
    try:
        data = BranchService.get_all(db)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{branch_id}")
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    try:
        data = BranchService.get_by_id(db, branch_id)
        if not data:
            raise HTTPException(status_code=404, detail="Branch not found")
        return {"status": "success", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/")
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    try:
        branch_id = BranchService.create(db, branch)
        return {"status": "success", "message": "Branch created successfully", "id": branch_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.put("/{branch_id}")
@router.patch("/{branch_id}")
def update_branch(branch_id: int, branch: BranchUpdate, db: Session = Depends(get_db)):
    try:
        updated = BranchService.update(db, branch_id, branch)
        if not updated:
            raise HTTPException(status_code=404, detail="Branch not found or no fields to update")
        return {"status": "success", "message": "Branch updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
