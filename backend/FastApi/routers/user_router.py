from fastapi import APIRouter, HTTPException
from models.users import User  

router = APIRouter(prefix="/users", tags=["Users"])

Users = [
    User(id=1, name="admin", email="admin@example.com", password="admin", is_admin=True),
    User(id=2, name="Bob", email="bob@example.com", password="password456", is_admin=False),
    User(id=3, name="Charlie", email="charlie@example.com", password="password789", is_admin=False),
    User(id=4, name="Alice", email="alice@example.com", password="password123", is_admin=False),
]

# Función auxiliar para buscar por ID
def find_user_by_id(user_id: int):
    for user in Users:
        if user.id == user_id:
            return user
    return None

# Listar todos los usuarios
@router.get("/")
async def list_users():
    return [user.dict() for user in Users]

# Obtener usuario por ID
@router.get("/{user_id}")
async def get_user(user_id: int):
    user = find_user_by_id(user_id)
    if user:
        return user.dict()
    raise HTTPException(status_code=404, detail="User not found")

# Crear usuario nuevo
@router.post("/")
async def create_user(user: User):
    if any(u.email == user.email for u in Users):
        raise HTTPException(status_code=400, detail="Email already registered")

    user.id = max(u.id for u in Users) + 1
    Users.append(user)
    return user
