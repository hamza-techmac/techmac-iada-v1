from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from queries import DateQueries  # type: ignore

class DateService:
    @staticmethod
    def get_all_dates(db: Session):
        return db.execute(text(DateQueries.GET_ALL)).mappings().all()
