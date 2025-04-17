def car_schema(car) -> dict:
    return {
        "id": str(car["_id"]),
        "brand": car["brand"],
        "model": car["model"],
        "year": car["year"],
        "color": car["color"],
        "price": car["price"],
        "is_available": car["is_available"],
        "mileage": car["mileage"],
        "engine_type": car["engine_type"],
        "transmission": car["transmission"],
        "fuel_type": car["fuel_type"],
        "doors": car["doors"],
        "seats": car["seats"],
        "max_speed": car["max_speed"],
        "acceleration": car["acceleration"],
        "horsepower": car["horsepower"],
        "torque": car["torque"],
        "weight": car["weight"],
        "length": car["length"],
        "width": car["width"],
        "description": car["description"],
        "image_url": car.get("image_url", ""),
        "paymenth_method": car["paymenth_method"],

        **({"history": car["history"]} if "history" in car else {})
    }


def cars_schema(cars) -> list:
    return [car_schema(car) for car in cars]