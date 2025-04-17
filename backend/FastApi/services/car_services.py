from bson import ObjectId
from models.cars import Car, CarHistory
from typing import List, Optional
from db.client import db_client
from db.schemas.cars import car_schema, cars_schema
from db.schemas.cars_history import carhistory_schema
from services.carhistory_service import get_car_history, create_car_history, delete_car_history, update_car_history

async def create_car(car: Car) -> Car:
    try:
        # Convertimos el objeto a dict, excluyendo el ID y la historia
        car_dict = car.dict(exclude={"id", "history"})
        car_history = getattr(car, "history", None)

        # Insertamos el coche en la base
        result = db_client.local.cars.insert_one(car_dict)
        car_id = str(result.inserted_id)

        # Creamos la historia si viene
        if car_history is not None:
            await create_car_history(car_id, car_history)

        # Obtenemos los datos insertados
        new_car_data = db_client.local.cars.find_one({"_id": result.inserted_id})
        car_data = car_schema(new_car_data)
        car_data["id"] = car_id

        # Cargamos la historia si existe en DB
        car_history_db = await get_car_history(car_id)
        if car_history_db:
            car_data["history"] = car_history_db

        return Car(**car_data)

    except Exception as e:
        raise RuntimeError(f"Error al crear el coche: {e}")


async def update_car(car_id: str, car: Car) -> Car:
    try:
        car_dict = dict(car)
        del car_dict["id"]
        car_history = car_dict.pop("history", None)
        await db_client.local.cars.update_one({"_id": car_id}, {"$set": car_dict})
        if car_history is not None:
            await update_car_history(car_id, car_history)
        return await get_car_by_id(car_id)
    except Exception as e:
        raise RuntimeError(f"Error al actualizar el coche: {e}")

def delete_car(car_id: str) -> bool:
    try:
        delete_car_history(car_id)
        result = db_client.local.cars.delete_one({"_id": car_id})
        return result.deleted_count > 0
    except Exception as e:
        raise RuntimeError(f"Error al eliminar el coche: {e}")

def linkcar_history(car_id: str, car_history: CarHistory) -> bool:
    try:
        create_car_history(car_id, car_history)
        return True
    except Exception as e:
        raise RuntimeError(f"Error al vincular el historial del coche: {e}")
    
async def get_car_by_id(car_id: str) -> Optional[Car]:
    try:
        car_data = await db_client.local.cars.find_one({"_id": ObjectId(car_id)})
        if car_data:
            car = car_schema(car_data)
            car["id"] = str(car_data["_id"])
            
            history_data = await db_client.local.car_histories.find_one({"car_id": car["id"]})
            if history_data:
                car["history"] = carhistory_schema(history_data)

            return Car(**car)
        return None
    except Exception as e:
        raise RuntimeError(f"Error al obtener el coche por ID: {e}")
    
def get_all_cars() -> List[Car]:
    try:
        cars_data = db_client.local.cars.find()
        return cars_schema(cars_data)
    except Exception as e:
        raise RuntimeError(f"Error al obtener todos los coches: {e}")
    