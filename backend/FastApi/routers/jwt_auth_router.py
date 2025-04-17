from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import login, get_current_user
from models.users import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await login(form_data)
    return {"message": "Login successful", "data": result}

@router.get("/me")
async def get_user_me(user: User = Depends(get_current_user)):
    return user
