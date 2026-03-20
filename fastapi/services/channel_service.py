from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import ChannelCreate, ChannelUpdate  # type: ignore
from queries import ChannelQueries  # type: ignore

class ChannelService:
    @staticmethod
    def get_all(db: Session):
        return db.execute(text(ChannelQueries.GET_ALL)).mappings().all()

    @staticmethod
    def get_by_id(db: Session, channel_id: int):
        return db.execute(text(ChannelQueries.GET_BY_ID), {"id": channel_id}).mappings().first()

    @staticmethod
    def create(db: Session, channel: ChannelCreate):
        query = text(ChannelQueries.INSERT)
        result = db.execute(query, channel.model_dump())
        db.commit()
        return result.lastrowid

    @staticmethod
    def update(db: Session, channel_id: int, channel: ChannelUpdate):
        update_data = channel.model_dump(exclude_unset=True)
        if not update_data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = text(ChannelQueries.update_query(set_clause))
        
        update_data["id"] = channel_id
        result = db.execute(query, update_data)
        db.commit()
        
        return result.rowcount > 0
