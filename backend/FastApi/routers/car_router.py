from fastapi import APIRouter, HTTPException
from models.cars import Car  
from services.car_services import *

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/")
def get_cars():
    try:
        return get_all_cars()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/newcar")
def create_new_car(car: Car):
    try:
        return create_car(car)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/updatecar/{car_id}")
def update_car_endpoint(car_id: str, car: Car):
    try:
        updated_car = update_car(car_id, car)
        if updated_car:
            return updated_car
        raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/deletecar/{car_id}")
def delete_car_endpoint(car_id: str):
    try:
        if delete_car(car_id):
            return {"message": "Car deleted successfully"}
        raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

