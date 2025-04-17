from pydantic import BaseModel

class CarHistory(BaseModel):
    id: int
    car_id: int
    action: str  # e.g., "viewed", "purchased", "inquired"
    accidents: list[str]  # List of accidents related to the car, if any
    service_records: list[str]  # List of service records related to the car, if any
    ownership_history: list[str]  # List of previous owners, if any
    last_updated: str  # Timestamp of the last update to the history record