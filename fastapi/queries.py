# queries.py
# This file centralizes all raw SQL queries used in the application.

class FranchiseQueries:
    GET_ALL = """
        SELECT id, franchise_name, owner_name, contact_email 
        FROM dim_franchise
    """

    INSERT = """
        INSERT INTO dim_franchise (franchise_name, owner_name, contact_email)
        VALUES (:franchise_name, :owner_name, :contact_email)
    """

    @staticmethod
    def update_query(set_clause: str) -> str:
        return f"UPDATE dim_franchise SET {set_clause} WHERE id = :id"

class BranchQueries:
    GET_ALL = "SELECT * FROM dim_branch"
    GET_BY_ID = "SELECT * FROM dim_branch WHERE id = :id"
    INSERT = """
        INSERT INTO dim_branch (franchise_id, branch_name, area_name, postcode, is_active, city_id)
        VALUES (:franchise_id, :branch_name, :area_name, :postcode, :is_active, :city_id)
    """
    
    @staticmethod
    def update_query(set_clause: str) -> str:
        return f"UPDATE dim_branch SET {set_clause} WHERE id = :id"

class ChannelQueries:
    GET_ALL = "SELECT * FROM dim_channel"
    GET_BY_ID = "SELECT * FROM dim_channel WHERE id = :id"
    INSERT = """
        INSERT INTO dim_channel (id, display_name, payment_method_id, provider_id)
        VALUES (:id, :display_name, :payment_method_id, :provider_id)
    """

    @staticmethod
    def update_query(set_clause: str) -> str:
        return f"UPDATE dim_channel SET {set_clause} WHERE id = :id"

class SaleQueries:
    INSERT_DIM_DATE = """
        INSERT IGNORE INTO dim_date 
        (date_key, sales_date, year, week_number, day_name, is_weekend)
        VALUES (:date_key, :sales_date, :year, :week_number, :day_name, :is_weekend)
    """
    INSERT_FACT_SALES = """
        INSERT INTO fact_sales (date_key, branch_id, channel_id, amount)
        VALUES (:date_key, :branch_id, :channel_id, :amount)
    """
    GET_DAYWISE_SALES = "SELECT * FROM vw_daywise_sales"

class DateQueries:
    GET_ALL = "SELECT * FROM dim_date"

class CityQueries:
    GET_ALL = "SELECT * FROM dim_city"
    GET_BY_ID = "SELECT * FROM dim_city WHERE id = :id"
    INSERT = """
        INSERT INTO dim_city (city_name, region)
        VALUES (:city_name, :region)
    """
    
    @staticmethod
    def update_query(set_clause: str) -> str:
        return f"UPDATE dim_city SET {set_clause} WHERE id = :id"

class RoleQueries:
    GET_ALL = "SELECT * FROM dim_roles"
    GET_BY_ID = "SELECT * FROM dim_roles WHERE id = :id"
    INSERT = "INSERT INTO dim_roles (name) VALUES (:name)"
    @staticmethod
    def update_query(set_clause: str) -> str: return f"UPDATE dim_roles SET {set_clause} WHERE id = :id"

class UserQueries:
    GET_ALL = "SELECT * FROM dim_users"
    GET_BY_ID = "SELECT * FROM dim_users WHERE id = :id"
    GET_BY_USERNAME = "SELECT * FROM dim_users WHERE username = :username"
    GET_BY_AUTH_KEY = "SELECT * FROM dim_users WHERE auth_key = :auth_key"
    INSERT = "INSERT INTO dim_users (username, password, auth_key, old_password, role_id) VALUES (:username, :password, :auth_key, :old_password, :role_id)"
    @staticmethod
    def update_query(set_clause: str) -> str: return f"UPDATE dim_users SET {set_clause} WHERE id = :id"

class PaymentMethodQueries:
    GET_ALL = "SELECT * FROM dim_payment_methods"
    GET_BY_ID = "SELECT * FROM dim_payment_methods WHERE id = :id"
    INSERT = "INSERT INTO dim_payment_methods (name) VALUES (:name)"
    @staticmethod
    def update_query(set_clause: str) -> str: return f"UPDATE dim_payment_methods SET {set_clause} WHERE id = :id"

class ProviderQueries:
    GET_ALL = "SELECT * FROM dim_providers"
    GET_BY_ID = "SELECT * FROM dim_providers WHERE id = :id"
    INSERT = "INSERT INTO dim_providers (name) VALUES (:name)"
    @staticmethod
    def update_query(set_clause: str) -> str: return f"UPDATE dim_providers SET {set_clause} WHERE id = :id"

class FranchiseActiveChannelQueries:
    GET_ALL = "SELECT * FROM franchise_active_channels"
    GET_BY_ID = "SELECT * FROM franchise_active_channels WHERE id = :id"
    INSERT = "INSERT INTO franchise_active_channels (branch_id, channel_id, is_active) VALUES (:branch_id, :channel_id, :is_active)"
    @staticmethod
    def update_query(set_clause: str) -> str: return f"UPDATE franchise_active_channels SET {set_clause} WHERE id = :id"
