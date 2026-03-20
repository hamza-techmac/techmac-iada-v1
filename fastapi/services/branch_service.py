from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import BranchCreate, BranchUpdate  # type: ignore
from queries import BranchQueries  # type: ignore

class BranchService:
    @staticmethod
    def get_all(db: Session):
        return db.execute(text(BranchQueries.GET_ALL)).mappings().all()

    @staticmethod
    def get_by_id(db: Session, branch_id: int):
        return db.execute(text(BranchQueries.GET_BY_ID), {"id": branch_id}).mappings().first()

    @staticmethod
    def create(db: Session, branch: BranchCreate):
        query = text(BranchQueries.INSERT)
        result = db.execute(query, branch.model_dump())
        db.commit()
        return result.lastrowid

    @staticmethod
    def update(db: Session, branch_id: int, branch: BranchUpdate):
        update_data = branch.model_dump(exclude_unset=True)
        if not update_data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = text(BranchQueries.update_query(set_clause))
        
        update_data["id"] = branch_id
        result = db.execute(query, update_data)
        db.commit()
        
        return result.rowcount > 0
