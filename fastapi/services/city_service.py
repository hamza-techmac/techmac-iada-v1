from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import CityCreate, CityUpdate  # type: ignore
from queries import CityQueries  # type: ignore

class CityService:
    @staticmethod
    def get_all(db: Session):
        return db.execute(text(CityQueries.GET_ALL)).mappings().all()

    @staticmethod
    def get_by_id(db: Session, city_id: int):
        return db.execute(text(CityQueries.GET_BY_ID), {"id": city_id}).mappings().first()

    @staticmethod
    def create(db: Session, city: CityCreate):
        query = text(CityQueries.INSERT)
        result = db.execute(query, city.model_dump())
        db.commit()
        return result.lastrowid

    @staticmethod
    def update(db: Session, city_id: int, city: CityUpdate):
        update_data = city.model_dump(exclude_unset=True)
        if not update_data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = text(CityQueries.update_query(set_clause))
        
        update_data["id"] = city_id
        result = db.execute(query, update_data)
        db.commit()
        
        return result.rowcount > 0
