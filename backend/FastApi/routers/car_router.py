from fastapi import APIRouter, HTTPException
from models.cars import Car  

router = APIRouter(prefix="/cars", tags=["Cars"])

cars = [
    Car(
        id=1,
        brand="Toyota",
        model="Corolla",
        year=2020,
        color="Blue",
        price=20000.0,
        is_available=True,
        mileage=15000,
        engine_type="Gasoline",
        transmission="Automatic",
        fuel_type="Petrol",
        doors=4,
        seats=5,
        description="A reliable and fuel-efficient sedan.",
        image_url=""
    ),
    Car(
        id=2,
        brand="Honda",
        model="Civic",
        year=2019,
        color="Red",
        price=22000.0,
        is_available=True,
        mileage=12000,
        engine_type="Gasoline",
        transmission="Manual",
        fuel_type="Petrol",
        doors=4,
        seats=5,
        description="A sporty and stylish compact car.",
        image_url=""
    )
]

@router.get("/")
async def get_all_cars():
    return [car.dict() for car in cars]

@router.get("/{car_id}")
async def get_car(car_id: int):
    for car in cars:
        if car.id == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")
