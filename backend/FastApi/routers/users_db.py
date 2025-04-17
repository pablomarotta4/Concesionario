from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.users import User, UserDb
from services.user_service import add_user, get_all_users, delete_user

router = APIRouter(prefix="/usersdb", tags=["userdb"])

list_users = get_all_users()

@router.get("/", response_model=list[User])
async def list_users_db():
    return list_users

@router.post("/register", response_model=User)
async def create_user_db(user: UserDb):
    try:
        return add_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
class DeleteUserRequest(BaseModel):
    username: str

@router.post("/delete", response_model=User)
async def delete_user_db(request: DeleteUserRequest):
    try:
        return delete_user(request.username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
