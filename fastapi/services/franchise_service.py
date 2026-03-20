from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import FranchiseCreate, FranchiseUpdate  # type: ignore
from queries import FranchiseQueries  # type: ignore

class FranchiseService:
    @staticmethod
    def get_all(db: Session):
        query = text(FranchiseQueries.GET_ALL)
        return db.execute(query).mappings().all()

    @staticmethod
    def create(db: Session, franchise: FranchiseCreate):
        query = text(FranchiseQueries.INSERT)
        result = db.execute(query, franchise.model_dump())
        db.commit()
        return result.lastrowid

    @staticmethod
    def update(db: Session, franchise_id: int, franchise: FranchiseUpdate):
        update_data = franchise.model_dump(exclude_unset=True)
        if not update_data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = text(FranchiseQueries.update_query(set_clause))
        
        update_data["id"] = franchise_id
        result = db.execute(query, update_data)
        db.commit()
        
        return result.rowcount > 0
