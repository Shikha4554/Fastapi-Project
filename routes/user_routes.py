from fastapi import APIRouter, Depends
from auth import get_current_user

router = APIRouter(prefix="/users")
@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    current_user.pop("hashed_password")
    return current_user
