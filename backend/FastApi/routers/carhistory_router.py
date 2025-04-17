from fastapi import APIRouter, Depends, HTTPException, status
from models import CarHistory
from services.carhistory_service import get_car_history, create_car_history

router = APIRouter(prefix="/carhistory", tags=["Car History"])

@router.get("/{car_id}", response_model=CarHistory, status_code=status.HTTP_200_OK)
async def read_car_history(car_id: int):
    history = await get_car_history(car_id)
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car history not found")
    return history

@router.post("/", response_model=CarHistory, status_code=status.HTTP_201_CREATED)
async def add_car_history(car_history: CarHistory):
    created_history = await create_car_history(car_history)
    return created_history
