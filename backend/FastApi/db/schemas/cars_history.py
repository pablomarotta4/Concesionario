def carhistory_schema (carhistory) -> dict:
    return {
        "id": str(carhistory["_id"]),
        "car_id": str(carhistory["car_id"]),
        "user_id": str(carhistory["user_id"]),
        "action": carhistory["action"],
        "timestamp": carhistory["timestamp"],
    }