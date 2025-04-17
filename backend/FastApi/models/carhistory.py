from typing import Optional
from pydantic import BaseModel

class CarHistory(BaseModel):
    id: Optional[str] = None  # Optional field for the history record's ID
    car_id: Optional[str] = None
    action: Optional[str] = None  # e.g., "viewed", "purchased", "inquired"
    accidents: Optional[list[str]] = None  # List of accidents related to the car, if any
    service_records: Optional[list[str]] = None  # List of service records related to the car, if any
    ownership_history: Optional[list[str]] = None  # List of previous owners, if any
    last_updated: Optional[str] = None  # Timestamp of the last update to the history record