from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base  # type: ignore

# Replace these values with your actual MySQL database credentials
# Format: mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/db_analysis"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # pool_pre_ping=True helps to check if the connection is still active before using it
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
