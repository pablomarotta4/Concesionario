def car_schema(car) -> dict:
    return {
        "id": str(car["_id"]),
        "brand": car["brand"],
        "model": car["model"],
        "year": car["year"],
        "price": car["price"],
        "mileage": car["mileage"],
        "color": car["color"],
        "description": car["description"],
        "image_url": car["image_url"],
    }