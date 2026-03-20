from fastapi import APIRouter, Depends, HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from schemas import CityCreate, CityUpdate  # type: ignore
from services.city_service import CityService  # type: ignore

router = APIRouter(prefix="/cities", tags=["Cities"])

@router.get("/")
def get_cities(db: Session = Depends(get_db)):
    try:
        data = CityService.get_all(db)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{city_id}")
def get_city(city_id: int, db: Session = Depends(get_db)):
    try:
        data = CityService.get_by_id(db, city_id)
        if not data:
            raise HTTPException(status_code=404, detail="City not found")
        return {"status": "success", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/")
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    try:
        city_id = CityService.create(db, city)
        return {"status": "success", "message": "City created successfully", "id": city_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.put("/{city_id}")
@router.patch("/{city_id}")
def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db)):
    try:
        updated = CityService.update(db, city_id, city)
        if not updated:
            raise HTTPException(status_code=404, detail="City not found or no fields to update")
        return {"status": "success", "message": "City updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
