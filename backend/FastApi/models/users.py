from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    username: str
    name: str
    email: EmailStr
    is_admin: bool

class UserDb(User):
    password: str