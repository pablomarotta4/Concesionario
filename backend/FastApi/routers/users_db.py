from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr
from models.users import User, UserDb
from services.user_service import (
    get_all_users_db,
    find_user_by_id_db,
    find_user_by_email_db,
    add_user_db,
    find_user_by_username_db,
)
from db.client import db_client

router = APIRouter(prefix="/usersdb", tags=["userdb"])

list_users = []

@router.get("/", response_model=list[User])
async def list_users_db():
    return list_users()

@router.post("/register", response_model=User)
async def create_user_db(user: UserDb):
    return None