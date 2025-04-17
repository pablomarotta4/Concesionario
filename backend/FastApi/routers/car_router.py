from fastapi import APIRouter, HTTPException
from models.cars import Car  
from services.car_services import *

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.get("/")
async def get_cars():
    return get_all_cars()

