from typing import List, Optional
from pydantic import BaseModel, EmailStr
from models.users import User, UserDb

Users: List[UserDb] = [
    UserDb(id=1, username="admin", name="admin", email="admin@example.com", password="$2a$12$RIKRgTo6hTAs.9cq0It6a.kh85bKrzEUPAHlMpkCGntasdY6w3PoK", is_admin=True),
    UserDb(id=2, username="bob", name="Bob", email="bob@example.com", password="$2a$12$TMM0NL0DUiXfWkoDavYzHed7qpF0qpjss2iWOm6ekHFdpNX29dhHa", is_admin=False),
    UserDb(id=3, username="charlie", name="Charlie", email="charlie@example.com", password="$2a$12$ygwk3JRCkQRPZX7CMLaeVO3JOh5PZFMOO6BJO8wtws.wRQom7138K", is_admin=False),
]

def get_all_users() -> List[User]:
    return [User(id=user.id, username=user.username, name=user.name, email=user.email, is_admin=user.is_admin) for user in Users]

def find_user_by_id(user_id: int) -> Optional[User]:
    user = next((u for u in Users if u.id == user_id), None)
    return User(id=user.id, username=user.username, name=user.name, email=user.email, is_admin=user.is_admin) if user else None

def find_user_by_email(email: str) -> Optional[User]:
    user = next((u for u in Users if u.email == email), None)
    return User(id=user.id, username=user.username, name=user.name, email=user.email, is_admin=user.is_admin) if user else None

def find_user_by_username(username: str) -> Optional[User]:
    user = next((u for u in Users if u.username == username), None)
    return User(id=user.id, username=user.username, name=user.name, email=user.email, is_admin=user.is_admin) if user else None

def find_user(input: str) -> Optional[User]:
    user = next((u for u in Users if u.username == input or u.email == input), None)
    return User(id=user.id, username=user.username, name=user.name, email=user.email, is_admin=user.is_admin) if user else None

def add_user(user: User, password: str) -> User:
    user_id = max(u.id for u in Users) + 1 if Users else 1
    new_user = UserDb(id=user_id, username=user.username, name=user.name, email=user.email, is_admin=user.is_admin, password=password)
    Users.append(new_user)
    return User(id=new_user.id, username=new_user.username, name=new_user.name, email=new_user.email, is_admin=new_user.is_admin)

def search_usersDB_returnPass(username: str) -> Optional[str]:
    user = next((u for u in Users if u.username == username), None)
    return user.password if user else None

def search_usersDB(username: str) -> UserDb:
    user = next((u for u in Users if u.username == username), None)
    return user 

def search_usersDB_returnId(username: str) -> Optional[int]:
    user = next((u for u in Users if u.username == username), None)
    return user.id if user else None