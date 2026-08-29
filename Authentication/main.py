from fastapi import FastAPI, Depends, HTTPException, status
from models import RegisterRequest, LoginRequest
from fastapi.security import HTTPAuthorizationCredentials

from auth import(
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
    http_bearer
)
app=FastAPI()


@app.get("/")
def main_page():
    return "Hello and Welcome to the Authentication Practice Fastapi Practice"

users = {}
next_user_id = 1


def get_current_user(
    credentials:HTTPAuthorizationCredentials = Depends(http_bearer)
):
    token = credentials.credentials
    payload = verify_token(token)
    user_id = int(payload["sub"])
    for user in users.values():
        if user["id"] ==user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

def require_admin(
    current_user = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins are allowed"
        )
    return current_user

#register user
@app.post("/auth/register")
def register(data:RegisterRequest):
    global next_user_id
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    hashed_password = hash_password(
        data.password
    )
    users[data.email] = {
        "id":next_user_id,
        "email":data.email,
        "password":hashed_password,
        "role":"user"
    }
    next_user_id +=1
    return {
        "message": "User registered successfully"
    }

@app.post("/auth/login")
def login(data: LoginRequest):
    user = users.get(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    password_is_valid = verify_password(
        data.password,
        user["password"],
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(
        user["id"],
        user["role"]
    )
    return{
        "access_token":access_token,
        "token_type": "bearer"
    }

@app.get("/users/me")
def read_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

@app.get("/admin/users")
def get_all_users(
    current_user = Depends(require_admin)
):
    return list(users.values())