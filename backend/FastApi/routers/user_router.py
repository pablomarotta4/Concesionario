from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from models.users import User, UserDb
from services.user_service import get_all_users, find_user_by_id, find_user_by_email, add_user, find_user_by_username

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/users", response_model=list[User])
async def list_users():
    return get_all_users()

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/register", response_model=User)
async def create_user(user: UserDb):
    # Validate that all required fields are present
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if field not in user.model_dump() or (field == "password" and not user.password):
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Check if email is already registered
    if find_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username is already registered
    if find_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create user in the database
    created_user = add_user(user, user.password)
    
    return created_user
