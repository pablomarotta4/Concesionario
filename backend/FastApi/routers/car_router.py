from fastapi import APIRouter, HTTPException
from models.cars import Car  
from services.car_services import *

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.get("/")
async def get_cars():
    return get_all_cars()

@router.post("/newcar")
async def create_new_car(car: Car, current_user: User = Depends(get_current_user)):
    try:
        return await create_car(car)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/updatecar/{car_id}")
async def update_car(car_id: str, car: Car):
    try:
        updated_car = update_car(car_id, car)
        if updated_car:
            return updated_car
        raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/deletecar/{car_id}")
async def delete_car(car_id: str):
    try:
        if delete_car(car_id):
            return {"message": "Car deleted successfully"}
        raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

