from sqlalchemy import create_engine, text  # type: ignore
from database import SQLALCHEMY_DATABASE_URL  # type: ignore

def create_tables():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_franchise (
                id INT AUTO_INCREMENT PRIMARY KEY,
                franchise_name VARCHAR(255) NOT NULL,
                owner_name VARCHAR(255) NOT NULL,
                contact_email VARCHAR(255) NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_city (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_name VARCHAR(255) NOT NULL,
                region VARCHAR(255)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_branch (
                id INT AUTO_INCREMENT PRIMARY KEY,
                franchise_id INT NOT NULL,
                branch_name VARCHAR(255) NOT NULL,
                area_name VARCHAR(255),
                postcode VARCHAR(50),
                is_active INT DEFAULT 1,
                city_id INT NOT NULL,
                FOREIGN KEY (franchise_id) REFERENCES dim_franchise(id),
                FOREIGN KEY (city_id) REFERENCES dim_city(id)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_roles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                auth_key VARCHAR(255),
                old_password VARCHAR(255),
                role_id INT NOT NULL,
                FOREIGN KEY (role_id) REFERENCES dim_roles(id)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_payment_methods (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_providers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_channel (
                id INT PRIMARY KEY,
                display_name VARCHAR(255) NOT NULL,
                payment_method_id INT NOT NULL,
                provider_id INT NOT NULL,
                FOREIGN KEY (payment_method_id) REFERENCES dim_payment_methods(id),
                FOREIGN KEY (provider_id) REFERENCES dim_providers(id)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS franchise_active_channels (
                id INT AUTO_INCREMENT PRIMARY KEY,
                branch_id INT NOT NULL,
                channel_id INT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (branch_id) REFERENCES dim_branch(id),
                FOREIGN KEY (channel_id) REFERENCES dim_channel(id)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_date (
                date_key INT PRIMARY KEY,
                sales_date DATE NOT NULL,
                year INT NOT NULL,
                week_number INT NOT NULL,
                day_name VARCHAR(50) NOT NULL,
                is_weekend INT NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_key INT NOT NULL,
                branch_id INT NOT NULL,
                channel_id INT NOT NULL,
                amount FLOAT NOT NULL,
                FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
                FOREIGN KEY (branch_id) REFERENCES dim_branch(id),
                FOREIGN KEY (channel_id) REFERENCES dim_channel(id)
            )
        """))

        conn.execute(text("""
            CREATE OR REPLACE VIEW vw_daywise_sales AS
            SELECT 
                d.sales_date,
                SUM(f.amount) as total_sales
            FROM fact_sales f
            JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.sales_date
        """))
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
