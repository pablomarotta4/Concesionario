from models.users import User, UserDb
from services.user_service import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")  

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 90
SECRET = "1e98911d53c5b64948b3ea50220409d2"

# Usar la misma configuración que en user_service.py
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = find_user_by_username(form_data.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    userP = search_usersDB(form_data.username)
    
    if not crypt.verify(form_data.password, userP.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expires
    access_token = {
        "sub": user_db.username,
        "exp": expire,
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    }

async def auth_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = find_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return user

async def get_current_user(user: User = Depends(auth_user)):
    return user