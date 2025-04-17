
from pydantic import EmailStr
from models.users import User, UserDb
from services.user_service import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

Users: List[UserDb] = get_all_users()

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = find_user(form_data.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if form_data.password != search_usersDB(form_data.username):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user_db.username, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2)):
    user_db = find_user(token)
    if user_db is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return user_db




