import sys  # type: ignore
import os  # type: ignore

# Append project root to sys path to resolve absolute imports locally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from database import get_db  # type: ignore
from schemas import UserLogin, LoginResponse  # type: ignore
from services.auth_service import AuthService  # type: ignore

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=None)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        auth_data = AuthService.login(db, credentials)
        if not auth_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"status": "success", "message": "Login successful", "data": auth_data}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
