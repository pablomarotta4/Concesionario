def carhistory_schema(carhistory) -> dict:
    return {
        "id": str(carhistory["_id"]),
        "car_id": str(carhistory["car_id"]),
        "action": carhistory["action"],
        "accidents": carhistory.get("accidents", []),
        "service_records": carhistory.get("service_records", []),
        "ownership_history": carhistory.get("ownership_history", []),
        "last_updated": carhistory.get("last_updated", ""),
    }

def carhistories_schema(carhistories) -> list:
    return [carhistory_schema(carhistory) for carhistory in carhistories]