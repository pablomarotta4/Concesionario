from models.cars import Car
from typing import List, Optional

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

def get_all_cars() -> List[Car]:
    return cars

def get_car_by_id(car_id: int) -> Optional[Car]:
    return next((car for car in cars if car.id == car_id), None)

def add_car(car: Car) -> None:
    cars.append(car)

def update_car(car_id: int, updated_car: Car) -> bool:
    for index, car in enumerate(cars):
        if car.id == car_id:
            cars[index] = updated_car
            return True
    return False

def delete_car(car_id: int) -> bool:
    for index, car in enumerate(cars):
        if car.id == car_id:
            del cars[index]
            return True
    return False