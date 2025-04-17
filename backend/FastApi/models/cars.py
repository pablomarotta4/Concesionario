from typing import Optional
from pydantic import BaseModel
from models.carhistory import CarHistory

class Car(BaseModel):
    id: Optional[str] = None
    brand: str
    model: str
    year: int
    color: str
    price: float
    is_available: bool
    mileage: int
    engine_type: str
    transmission: str
    fuel_type: str
    doors: int
    seats: int
    max_speed: Optional[int] = None
    acceleration: float
    horsepower: int
    torque: int
    weight: int
    length: float
    width: float
    description: str
    image_url: Optional[str] = None
    paymenth_method: str 
    history: Optional[CarHistory] = None  
    
