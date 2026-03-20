from fastapi import APIRouter, Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from services.date_service import DateService  # type: ignore

router = APIRouter(prefix="/dates", tags=["Dates"])

@router.get("/")
def get_dates(db: Session = Depends(get_db)):
    try:
        data = DateService.get_all_dates(db)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
