from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import PaymentMethodCreate, PaymentMethodUpdate  # type: ignore
from queries import PaymentMethodQueries  # type: ignore

class PaymentMethodService:
    @staticmethod
    def get_all(db: Session):
        return db.execute(text(PaymentMethodQueries.GET_ALL)).mappings().all()

    @staticmethod
    def get_by_id(db: Session, entity_id: int):
        return db.execute(text(PaymentMethodQueries.GET_BY_ID), {"id": entity_id}).mappings().first()

    @staticmethod
    def create(db: Session, entity: PaymentMethodCreate):
        query = text(PaymentMethodQueries.INSERT)
        result = db.execute(query, entity.model_dump())
        db.commit()
        return result.lastrowid

    @staticmethod
    def update(db: Session, entity_id: int, entity: PaymentMethodUpdate):
        update_data = entity.model_dump(exclude_unset=True)
        if not update_data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = text(PaymentMethodQueries.update_query(set_clause))
        
        update_data["id"] = entity_id
        result = db.execute(query, update_data)
        db.commit()
        
        return result.rowcount > 0
