from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import ProviderCreate, ProviderUpdate  # type: ignore
from queries import ProviderQueries  # type: ignore

class ProviderService:
    @staticmethod
    def get_all(db: Session):
        return db.execute(text(ProviderQueries.GET_ALL)).mappings().all()

    @staticmethod
    def get_by_id(db: Session, entity_id: int):
        return db.execute(text(ProviderQueries.GET_BY_ID), {"id": entity_id}).mappings().first()

    @staticmethod
    def create(db: Session, entity: ProviderCreate):
        query = text(ProviderQueries.INSERT)
        result = db.execute(query, entity.model_dump())
        db.commit()
        return result.lastrowid

    @staticmethod
    def update(db: Session, entity_id: int, entity: ProviderUpdate):
        update_data = entity.model_dump(exclude_unset=True)
        if not update_data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = text(ProviderQueries.update_query(set_clause))
        
        update_data["id"] = entity_id
        result = db.execute(query, update_data)
        db.commit()
        
        return result.rowcount > 0
