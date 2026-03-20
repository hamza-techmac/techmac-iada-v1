from fastapi import FastAPI, Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from database import get_db  # type: ignore
from dependencies import get_current_user  # type: ignore

from routers import (  # type: ignore
    franchises, branches, channels, sales, dates, cities,
    roles, users, payment_methods, providers, franchise_active_channels,
    auth
)

app = FastAPI()

# Apply auth dependency to all business endpoints
app.include_router(franchises.router, dependencies=[Depends(get_current_user)])
app.include_router(branches.router, dependencies=[Depends(get_current_user)])
app.include_router(channels.router, dependencies=[Depends(get_current_user)])
app.include_router(sales.router, dependencies=[Depends(get_current_user)])
app.include_router(dates.router, dependencies=[Depends(get_current_user)])
app.include_router(cities.router, dependencies=[Depends(get_current_user)])
app.include_router(roles.router, dependencies=[Depends(get_current_user)])
app.include_router(users.router, dependencies=[Depends(get_current_user)])
app.include_router(payment_methods.router, dependencies=[Depends(get_current_user)])
app.include_router(providers.router, dependencies=[Depends(get_current_user)])
app.include_router(franchise_active_channels.router, dependencies=[Depends(get_current_user)])

# Exclude auth dependency from the login endpoint
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db_name = db.execute(text("SELECT DATABASE()")).scalar()
        tables = [row[0] for row in db.execute(text("SHOW TABLES")).fetchall()]
        return {"status": "success", "message": "Database connection established successfully!", "database": db_name, "tables": tables}
    except Exception as e:
        return {"status": "error", "message": str(e)}
