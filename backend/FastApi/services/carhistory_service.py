from fastapi import APIRouter, Depends, HTTPException, status
from models import CarHistory

router = APIRouter(prefix="/carhistory", tags=["Car History"])

car_histories = [
    CarHistory(
        id=1,
        car_id=1,
        action="viewed",
        accidents=["Fender bender in 2021"],
        service_records=["Oil change - Jan 2023", "Brake pads replaced - Jul 2022"],
        ownership_history=["John Doe", "Jane Smith"],
        last_updated="2024-12-01T15:30:00"
    ),
    CarHistory(
        id=2,
        car_id=2,
        action="purchased",
        accidents=[],
        service_records=["Tire rotation - Mar 2023"],
        ownership_history=["Carlos Ruiz"],
        last_updated="2025-01-10T10:00:00"
    )
]

async def get_car_history(car_id: int):
    for history in car_histories:
        if history.car_id == car_id:
            return history

async def create_car_history(car_history: CarHistory):
    car_histories.append(car_history)
    return car_history
