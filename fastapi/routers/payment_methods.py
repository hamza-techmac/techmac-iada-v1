from fastapi import APIRouter, Depends, HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from schemas import PaymentMethodCreate, PaymentMethodUpdate  # type: ignore
from services.payment_method_service import PaymentMethodService  # type: ignore

router = APIRouter(prefix="/payment_methods", tags=["PaymentMethods"])

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    try:
        data = PaymentMethodService.get_all(db)
        return {"status": "success", "data": [dict(row) for row in data]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        data = PaymentMethodService.get_by_id(db, id)
        if not data:
            raise HTTPException(status_code=404, detail="Not found")
        return {"status": "success", "data": dict(data)}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/")
def create(entity: PaymentMethodCreate, db: Session = Depends(get_db)):
    try:
        new_id = PaymentMethodService.create(db, entity)
        return {"status": "success", "message": "Created successfully", "id": new_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.put("/{id}")
@router.patch("/{id}")
def update(id: int, entity: PaymentMethodUpdate, db: Session = Depends(get_db)):
    try:
        updated = PaymentMethodService.update(db, id, entity)
        if not updated:
            raise HTTPException(status_code=404, detail="Not found or no fields to update")
        return {"status": "success", "message": "Updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
