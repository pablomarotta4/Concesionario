from pydantic import BaseModel

class Car(BaseModel):
    id: int
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
    description: str
    image_url: str
