from models.cars import Car, CarHistory
from typing import List, Optional

car_histories = [
    CarHistory(
        id=101,
        car_id=1,
        action="viewed",
        accidents=["Leve rayón en puerta izquierda (2022)"],
        service_records=["Cambio de aceite - 2023-05-15", "Cambio de pastillas de freno - 2024-02-10"],
        ownership_history=["Juan Pérez"],
        last_updated="2025-04-17T14:30:00Z"
    ),
    CarHistory(
        id=102,
        car_id=2,
        action="inquired",
        accidents=[],
        service_records=["Revisión completa - 2024-06-10"],
        ownership_history=["Lucía Rodríguez", "Martín Silva"],
        last_updated="2025-04-17T15:00:00Z"
    )
]

cars = [
    Car(
        id=1,
        brand="Toyota",
        model="Corolla",
        year=2021,
        color="Gray",
        price=18500.0,
        is_available=True,
        mileage=28000,
        engine_type="1.8L I4",
        transmission="Automatic",
        fuel_type="Petrol",
        doors=4,
        seats=5,
        max_speed=180,
        acceleration=10.2,
        horsepower=139,
        torque=126,
        weight=1310,
        length=4.62,
        width=1.78,
        description="Sedán cómodo, ideal para ciudad y carretera.",
        image_url="https://example.com/images/corolla2021.png",
        paymenth_method="Financing",
        history=car_histories[0]
    ),
    Car(
        id=2,
        brand="Ford",
        model="Focus",
        year=2018,
        color="White",
        price=15500.0,
        is_available=False,
        mileage=39000,
        engine_type="2.0L I4",
        transmission="Manual",
        fuel_type="Petrol",
        doors=4,
        seats=5,
        max_speed=200,
        acceleration=8.5,
        horsepower=160,
        torque=146,
        weight=1350,
        length=4.53,
        width=1.80,
        description="Vehículo compacto con buen rendimiento y respuesta.",
        image_url="https://example.com/images/focus2018.png",
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