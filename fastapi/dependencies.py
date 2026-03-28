from fastapi import Header, HTTPException

def get_current_user(authorization: str = Header(None)):
    # Placeholder: allows access for now
    return {"username": "admin"}
