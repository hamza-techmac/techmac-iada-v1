from fastapi import APIRouter, Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from schemas import SaleCreate  # type: ignore
from services.sale_service import SaleService  # type: ignore

router = APIRouter(tags=["Sales"])

@router.post("/sales")
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        SaleService.create_sale(db, sale)
        return {"status": "success", "message": "Sale record inserted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/daywise-sales")
def get_daywise_sales(db: Session = Depends(get_db)):
    try:
        data = SaleService.get_daywise_sales(db)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
