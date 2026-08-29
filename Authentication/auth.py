from datetime import datetime, timedelta, timezone


import jwt #type: ignore
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pwdlib import PasswordHash #type: ignore

password_hash = PasswordHash.recommended()

def hash_password(password:str):
    return password_hash.hash(password)

def verify_password(password:str,hashed_password:str) -> bool:
    return password_hash.verify(password,hashed_password)

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int,role:str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub":str(user_id),
        "role":role,
        "exp":expire
    }
    token = jwt.encode(payload,SECRET_KEY,ALGORITHM)
    return token

http_bearer = HTTPBearer()

def verify_token(token:str) -> dict:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authentication"
            )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication"
        )