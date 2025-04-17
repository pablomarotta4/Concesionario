from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    is_admin: bool

class UserDb(User):
    password: str