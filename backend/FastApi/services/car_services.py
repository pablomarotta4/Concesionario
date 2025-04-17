from models import Car, CarHistory 
from typing import List, Optional

cars = [
    Car(
        id=1,
        brand="Toyota",
        model="Corolla",
        year=2020,
        color="Blue",
        price=18900.0,
        is_available=True,
        mileage=25000,
        engine_type="Inline-4",
        transmission="Automatic",
        fuel_type="Petrol",
        doors=4,
        seats=5,
        max_speed=180,
        acceleration=10.5,
        horsepower=132,
        torque=128,
        weight=1300,
        length=4.62,
        width=1.77,
        description="Reliable and fuel-efficient sedan.",
        image_url="https://example.com/images/corolla.png",
        paymenth_method="Financing",
        history=car_histories[0]
    ),
    Car(
        id=2,
        brand="Honda",
        model="Civic",
        year=2019,
        color="Red",
        price=20500.0,
        is_available=False,
        mileage=31000,
        engine_type="Inline-4 Turbo",
        transmission="Manual",
        fuel_type="Petrol",
        doors=4,
        seats=5,
        max_speed=200,
        acceleration=8.7,
        horsepower=158,
        torque=138,
        weight=1275,
        length=4.67,
        width=1.80,
        description="Sporty compact car with great handling.",
        image_url="https://example.com/images/civic.png",
        paymenth_method="Cash",
        history=car_histories[1]
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