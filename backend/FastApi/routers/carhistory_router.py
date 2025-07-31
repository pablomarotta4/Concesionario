from fastapi import APIRouter, Depends, HTTPException, status
from models.carhistory import CarHistory
from services.carhistory_service import get_car_history, create_car_history, delete_car_history, update_car_history

router = APIRouter(prefix="/carhistory", tags=["Car History"])

@router.get("/")
async def get_car_history_endpoint(car_id: str):
    try:
        car_history = get_car_history(car_id)
        if car_history:
            return car_history
        raise HTTPException(status_code=404, detail="Car history not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/newcarhistory")
async def create_car_history_endpoint(car_history: CarHistory):
    try:
        return create_car_history(car_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/updatecarhistory/{car_id}")
async def update_car_history_endpoint(car_id: str, car_history: CarHistory):
    try:
        updated_car_history = update_car_history(car_id, car_history)
        if updated_car_history:
            return updated_car_history
        raise HTTPException(status_code=404, detail="Car history not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/deletecarhistory/{car_id}")
async def delete_car_history_endpoint(car_id: str):
    try:
        if delete_car_history(car_id):
            return {"message": "Car history deleted successfully"}
        raise HTTPException(status_code=404, detail="Car history not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
