from typing import List, Optional
from models.users import User, UserDb
from db.client import db_client
from db.schemas.users import user_schema


class UserAlreadyExistsError(Exception):
    """Excepción personalizada para indicar que un usuario ya existe."""
    pass


class UserNotFoundError(Exception):
    """Excepción personalizada para indicar que un usuario no fue encontrado."""
    pass


Users: List[UserDb] = []


def get_user_by_username(username: str) -> Optional[UserDb]:
    try:
        user_data = db_client.local.users.find_one({"username": username})
        if user_data:
            return UserDb(**user_schema(user_data))
        return None
    except Exception as e:
        raise RuntimeError(f"Error al buscar usuario por nombre de usuario: {e}")


def get_user_by_email(email: str) -> Optional[UserDb]:
    try:
        user_data = db_client.local.users.find_one({"email": email})
        if user_data:
            return UserDb(**user_schema(user_data))
        return None
    except Exception as e:
        raise RuntimeError(f"Error al buscar usuario por correo electrónico: {e}")


def get_all_users() -> List[UserDb]:
    try:
        users_data = db_client.local.users.find()
        return [UserDb(**user_schema(user)) for user in users_data]
    except Exception as e:
        raise RuntimeError(f"Error al obtener todos los usuarios: {e}")


def user_exists(username: str) -> bool:
    try:
        return db_client.local.users.find_one({"username": username}) is not None
    except Exception as e:
        raise RuntimeError(f"Error al verificar si el usuario existe: {e}")


def add_user(user: UserDb) -> UserDb:
    try:
        if user_exists(user.username):
            raise UserAlreadyExistsError(f"El nombre de usuario '{user.username}' ya existe.")
        user_dict = dict(user)
        del user_dict["id"]
        id = db_client.local.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.local.users.find_one({"_id": id}))
        return UserDb(**new_user)
    except UserAlreadyExistsError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Error al agregar un nuevo usuario: {e}")


def find_user_by_id(user_id: int) -> Optional[UserDb]:
    try:
        user_data = db_client.local.users.find_one({"id": user_id})
        if user_data:
            return UserDb(**user_schema(user_data))
        raise UserNotFoundError(f"Usuario con ID '{user_id}' no encontrado.")
    except UserNotFoundError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Error al buscar usuario por ID: {e}")

def delete_user(user_id: int) -> bool:
    try:
        result = db_client.local.users.delete_one({"id": user_id})
        if result.deleted_count == 0:
            raise UserNotFoundError(f"Usuario con ID '{user_id}' no encontrado.")
        return True
    except UserNotFoundError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Error al eliminar usuario: {e}")
    
    