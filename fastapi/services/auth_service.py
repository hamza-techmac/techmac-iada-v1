from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import text  # type: ignore
from schemas import UserLogin  # type: ignore
from queries import UserQueries  # type: ignore
import uuid  # type: ignore

class AuthService:
    @staticmethod
    def login(db: Session, credentials: UserLogin):
        # Fetch user by username
        user = db.execute(text(UserQueries.GET_BY_USERNAME), {"username": credentials.username}).mappings().first()
        
        if not user:
            return None
            
        # Verify password using bcrypt
        import passlib.hash  # type: ignore
        pwd_context = passlib.hash.bcrypt
        if not pwd_context.verify(credentials.password, user["password"]):
            return None

        # Generate a new 32-character auth token
        new_auth_key = uuid.uuid4().hex
        
        # Update user with the new auth_key
        set_clause = "auth_key = :auth_key"
        update_query = text(UserQueries.update_query(set_clause))
        
        db.execute(update_query, {"auth_key": new_auth_key, "id": user["id"]})
        db.commit()

        # Return the updated user info along with the token
        return {
            "id": user["id"],
            "username": user["username"],
            "role_id": user["role_id"],
            "auth_key": new_auth_key
        }
