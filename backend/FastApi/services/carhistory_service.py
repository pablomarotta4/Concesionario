from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models.carhistory import CarHistory
from db.client import get_database
from db.schemas.cars_history import carhistory_schema, carhistories_schema

def get_car_histories_collection():
    """Obtener la colección de historiales de autos"""
    db = get_database()
    return db.car_histories

def create_car_history(car_id: str, car_history: CarHistory) -> CarHistory:
    try:
        car_history_dict = car_history.dict(exclude={"id"})
        car_history_dict["car_id"] = car_id
        result = get_car_histories_collection().insert_one(car_history_dict)
        saved_doc = get_car_histories_collection().find_one({"_id": result.inserted_id})
        history_data = carhistory_schema(saved_doc)
        history_data["id"] = str(saved_doc["_id"])
        return CarHistory(**history_data)
    except Exception as e:
        raise RuntimeError(f"Error al crear el historial del coche: {e}")

def get_car_history(car_id: str) -> CarHistory:
    try:
        car_history_data = get_car_histories_collection().find_one({"car_id": car_id})
        if car_history_data:
            return CarHistory(**carhistory_schema(car_history_data))
        return None
    except Exception as e:
        raise RuntimeError(f"Error al obtener el historial del coche: {e}")
    
def get_all_car_histories() -> List[CarHistory]:
    try:
        car_histories_data = get_car_histories_collection().find()
        return carhistories_schema(car_histories_data)
    except Exception as e:
        raise RuntimeError(f"Error al obtener todos los historiales de coches: {e}")
    
def update_car_history(car_id: str, car_history: CarHistory) -> CarHistory:
    try:
        car_history_dict = dict(car_history)
        del car_history_dict["id"]
        get_car_histories_collection().update_one({"car_id": car_id}, {"$set": car_history_dict})
        return get_car_history(car_id)
    except Exception as e:
        raise RuntimeError(f"Error al actualizar el historial del coche: {e}")
    
def delete_car_history(car_id: str) -> bool:
    try:
        result = get_car_histories_collection().delete_one({"car_id": car_id})
        return result.deleted_count > 0
    except Exception as e:
        raise RuntimeError(f"Error al eliminar el historial del coche: {e}")