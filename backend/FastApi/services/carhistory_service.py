from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models.carhistory import CarHistory
from db.client import db_client
from db.schemas.cars_history import carhistory_schema, carhistories_schema

async def create_car_history(car_id: str, car_history: CarHistory) -> CarHistory:
    try:
        car_history_dict = car_history.dict(exclude={"id"})
        car_history_dict["car_id"] = car_id  # esto debe ser el ID real del auto
        result = db_client.local.car_histories.insert_one(car_history_dict)
        saved_doc = db_client.local.car_histories.find_one({"_id": result.inserted_id})
        history_data = carhistory_schema(saved_doc)
        history_data["id"] = str(saved_doc["_id"])
        return CarHistory(**history_data)

    except Exception as e:
        raise RuntimeError(f"Error al crear el historial del coche: {e}")

async def get_car_history(car_id: str) -> CarHistory:
    try:
        car_history_data = db_client.local.car_histories.find_one({"car_id": car_id})
        if car_history_data:
            return CarHistory(**carhistory_schema(car_history_data))
        return None
    except Exception as e:
        raise RuntimeError(f"Error al obtener el historial del coche: {e}")
    
async def get_all_car_histories() -> List[CarHistory]:
    try:
        car_histories_data = db_client.local.car_histories.find()
        return carhistories_schema(car_histories_data)
    except Exception as e:
        raise RuntimeError(f"Error al obtener todos los historiales de coches: {e}")
    
async def update_car_history(car_id: str, car_history: CarHistory) -> CarHistory:
    try:
        car_history_dict = dict(car_history)
        del car_history_dict["id"]
        db_client.local.car_histories.update_one({"car_id": car_id}, {"$set": car_history_dict})
        return get_car_history(car_id)
    except Exception as e:
        raise RuntimeError(f"Error al actualizar el historial del coche: {e}")
    
async def delete_car_history(car_id: str) -> bool:
    try:
        result = db_client.local.car_histories.delete_one({"car_id": car_id})
        return result.deleted_count > 0
    except Exception as e:
        raise RuntimeError(f"Error al eliminar el historial del coche: {e}")