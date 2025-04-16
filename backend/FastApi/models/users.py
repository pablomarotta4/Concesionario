from fastapi import FastAPI
from pydantic import BaseModel
# from sqlalchemy import Column, Integer, String, Boolean
# from backend.FastApi.database.db import Base

app = FastAPI()

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     password = Column(String, nullable=False)
#     is_admin = Column(Boolean, default=False)

class User(BaseModel):
        id: int
        name: str
        email: str
        password: str
        is_admin: bool
    
Users = [
    User(id=1, name="admin", email="admin@example.com", password="admin", is_admin=True),
    User(id=2, name="Bob", email="bob@example.com", password="password456", is_admin=False),
    User(id=3, name="Charlie", email="charlie@example.com", password="password789", is_admin=False),
    User(id=4, name="Alice", email="alice@example.com", password="password123", is_admin=False)
]

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return find_user_by_id(user_id)

def find_user_by_id(user_id: int):
    user = filter(lambda u: u.id == user_id, Users)
    try:
        return list(user)[0]
    except IndexError:
        return {"error": "User not found"}
    

@app.get("/userclass")
async def userclass():
    return Users 

@app.post("/users")
async def create_user(user: User):
    if any(u.email == user.email for u in Users):
        return {"error": "Email already registered"}
    elif any(u.id == user.id for u in Users):
        user.id = max(u.id for u in Users) + 1
        Users.append(user)
    else:
        Users.append(user)
    return user
