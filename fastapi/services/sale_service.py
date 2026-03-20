from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import SaleCreate  # type: ignore
from utils.date_utils import extract_date_dimensions  # type: ignore
from queries import SaleQueries  # type: ignore

class SaleService:
    @staticmethod
    def create_sale(db: Session, sale: SaleCreate):
        # Prepare date dimension attributes
        dim_date_data = extract_date_dimensions(sale.sales_date)

        # Insert into dim_date if the date_key doesn't already exist
        dim_date_query = text(SaleQueries.INSERT_DIM_DATE)
        db.execute(dim_date_query, dim_date_data)

        # Insert into fact_sales
        fact_sales_query = text(SaleQueries.INSERT_FACT_SALES)
        db.execute(fact_sales_query, {
            "date_key": dim_date_data["date_key"],
            "branch_id": sale.branch_id,
            "channel_id": sale.channel_id,
            "amount": sale.amount
        })
        db.commit()

    @staticmethod
    def get_daywise_sales(db: Session):
        return db.execute(text(SaleQueries.GET_DAYWISE_SALES)).mappings().all()
