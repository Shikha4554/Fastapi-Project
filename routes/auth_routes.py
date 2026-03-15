from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from models import UserRegister, UserResponse
from auth import authenticate_user, create_access_token, hash_password
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database.database import users_collection

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register_user(user: UserRegister):

    if users_collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    if users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pwd = hash_password(user.password)

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    user_dict = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hashed_pwd,
        "access_token": access_token,
        "disabled": False
    }

    result = users_collection.insert_one(user_dict)

    return {
        "user": {
            "id": str(result.inserted_id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        },
        "token": {
            "access_token": access_token,
            "token_type": "bearer"
        }
    }


#LOGIN

from models import TokenResponse

@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"access_token": access_token}}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
