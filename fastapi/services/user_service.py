from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import UserCreate, UserUpdate  # type: ignore
from queries import UserQueries  # type: ignore

class UserService:
    @staticmethod
    def get_all(db: Session):
        return db.execute(text(UserQueries.GET_ALL)).mappings().all()

    @staticmethod
    def get_by_id(db: Session, entity_id: int):
        return db.execute(text(UserQueries.GET_BY_ID), {"id": entity_id}).mappings().first()

    @staticmethod
    def create(db: Session, entity: UserCreate):
        import passlib.hash  # type: ignore
        entity.password = passlib.hash.bcrypt.hash(entity.password)
        query = text(UserQueries.INSERT)
        result = db.execute(query, entity.model_dump())
        db.commit()
        return result.lastrowid

    @staticmethod
    def update(db: Session, entity_id: int, entity: UserUpdate):
        update_data = entity.model_dump(exclude_unset=True)
        if not update_data:
            return False

        if "password" in update_data:
            import passlib.hash  # type: ignore
            update_data["password"] = passlib.hash.bcrypt.hash(update_data["password"])

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = text(UserQueries.update_query(set_clause))
        
        update_data["id"] = entity_id
        result = db.execute(query, update_data)
        db.commit()
        
        return result.rowcount > 0
