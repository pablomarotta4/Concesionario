"""
Script de seed para inicializar la base de datos con datos de prueba
Ejecutar desde la raíz del proyecto FastApi:
    python seed_database.py
"""

import sys
from pathlib import Path
import bcrypt
from db.client import get_database
from datetime import datetime
import os

def hash_password(password: str) -> str:
    """Hash de contraseña usando bcrypt directamente compatible con passlib"""
    # bcrypt genera hashes en formato $2b$ que son totalmente compatibles con passlib
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def seed_users():
    """Crea usuarios de prueba en la base de datos"""
    db = get_database()
    users_collection = db["users"]
    
    # Limpiar usuarios existentes (opcional - comentar si no quieres eliminar)
    # users_collection.delete_many({})
    
    users = [
        {
            "username": "admin",
            "name": "Administrador",
            "email": "admin@concesionario.com",
            "password": hash_password("admin123"),
            "is_admin": True,
            "disabled": False
        },
        {
            "username": "pmarotta",
            "name": "Pablo Marotta",
            "email": "pablo@example.com",
            "password": hash_password("password123"),
            "is_admin": False,
            "disabled": False
        },
        {
            "username": "jperez",
            "name": "Juan Pérez",
            "email": "juan.perez@example.com",
            "password": hash_password("password123"),
            "is_admin": False,
            "disabled": False
        },
        {
            "username": "mgarcia",
            "name": "María García",
            "email": "maria.garcia@example.com",
            "password": hash_password("password123"),
            "is_admin": False,
            "disabled": False
        },
        {
            "username": "lrodriguez",
            "name": "Luis Rodríguez",
            "email": "luis.rodriguez@example.com",
            "password": hash_password("password123"),
            "is_admin": True,
            "disabled": False
        }
    ]
    
    inserted_count = 0
    for user in users:
        # Verificar si el usuario ya existe
        existing_user = users_collection.find_one({"username": user["username"]})
        if not existing_user:
            users_collection.insert_one(user)
            inserted_count += 1
            print(f"✓ Usuario creado: {user['username']} ({user['email']})")
        else:
            print(f"⊘ Usuario ya existe: {user['username']}")
    
    print(f"\n{inserted_count} usuarios nuevos creados.")
    return inserted_count

def seed_cars():
    """Crea autos de prueba en la base de datos"""
    db = get_database()
    cars_collection = db["cars"]
    
    # Limpiar autos existentes (opcional - comentar si no quieres eliminar)
    # cars_collection.delete_many({})
    
    cars = [
        {
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "color": "Plateado",
            "price": 18500.00,
            "is_available": True,
            "mileage": 45000,
            "engine_type": "4 cilindros en línea",
            "transmission": "Automática CVT",
            "fuel_type": "Nafta",
            "doors": 4,
            "seats": 5,
            "max_speed": 180,
            "acceleration": 9.2,
            "horsepower": 132,
            "torque": 162,
            "weight": 1330,
            "length": 4.63,
            "width": 1.78,
            "description": "Sedán confiable y económico, ideal para uso diario",
            "image_url": "corolla2020.JPG",
            "paymenth_method": "Efectivo"
        },
        {
            "brand": "Honda",
            "model": "Civic",
            "year": 2019,
            "color": "Negro",
            "price": 17800.00,
            "is_available": True,
            "mileage": 52000,
            "engine_type": "4 cilindros en línea turbo",
            "transmission": "Manual 6 velocidades",
            "fuel_type": "Nafta",
            "doors": 4,
            "seats": 5,
            "max_speed": 200,
            "acceleration": 7.5,
            "horsepower": 174,
            "torque": 220,
            "weight": 1350,
            "length": 4.65,
            "width": 1.80,
            "description": "Deportivo y eficiente, con tecnología avanzada",
            "image_url": "civic2019.jpg",
            "paymenth_method": "Financiado"
        },
        {
            "brand": "BMW",
            "model": "X3",
            "year": 2021,
            "color": "Azul",
            "price": 45000.00,
            "is_available": True,
            "mileage": 28000,
            "engine_type": "4 cilindros turbo",
            "transmission": "Automática 8 velocidades",
            "fuel_type": "Diesel",
            "doors": 5,
            "seats": 5,
            "max_speed": 210,
            "acceleration": 6.3,
            "horsepower": 190,
            "torque": 400,
            "weight": 1850,
            "length": 4.71,
            "width": 1.89,
            "description": "SUV premium con tecnología de punta",
            "image_url": "bmw_x3_blue.jpg",
            "paymenth_method": "Efectivo"
        },
        {
            "brand": "Mercedes-Benz",
            "model": "C-Class",
            "year": 2022,
            "color": "Negro",
            "price": 52000.00,
            "is_available": True,
            "mileage": 15000,
            "engine_type": "4 cilindros turbo mild-hybrid",
            "transmission": "Automática 9G-TRONIC",
            "fuel_type": "Nafta",
            "doors": 4,
            "seats": 5,
            "max_speed": 250,
            "acceleration": 6.0,
            "horsepower": 204,
            "torque": 300,
            "weight": 1640,
            "length": 4.75,
            "width": 1.82,
            "description": "Lujo y rendimiento en perfecta armonía",
            "image_url": "mercedes_c_black.jpg",
            "paymenth_method": "Financiado"
        },
        {
            "brand": "Audi",
            "model": "A4",
            "year": 2020,
            "color": "Gris",
            "price": 38000.00,
            "is_available": True,
            "mileage": 35000,
            "engine_type": "4 cilindros turbo",
            "transmission": "Automática S tronic 7 velocidades",
            "fuel_type": "Nafta",
            "doors": 4,
            "seats": 5,
            "max_speed": 230,
            "acceleration": 6.7,
            "horsepower": 190,
            "torque": 320,
            "weight": 1575,
            "length": 4.76,
            "width": 1.85,
            "description": "Elegancia alemana con tecnología quattro",
            "image_url": "audi_a4_gray.jpg",
            "paymenth_method": "Efectivo"
        },
        {
            "brand": "Ford",
            "model": "Focus",
            "year": 2019,
            "color": "Blanco",
            "price": 14500.00,
            "is_available": True,
            "mileage": 62000,
            "engine_type": "3 cilindros turbo",
            "transmission": "Manual 6 velocidades",
            "fuel_type": "Nafta",
            "doors": 5,
            "seats": 5,
            "max_speed": 180,
            "acceleration": 9.8,
            "horsepower": 125,
            "torque": 170,
            "weight": 1285,
            "length": 4.38,
            "width": 1.83,
            "description": "Compacto versátil con gran equipamiento",
            "image_url": "ford_focus_white.jpg",
            "paymenth_method": "Financiado"
        },
        {
            "brand": "Volkswagen",
            "model": "Golf GTI",
            "year": 2021,
            "color": "Rojo",
            "price": 32000.00,
            "is_available": True,
            "mileage": 22000,
            "engine_type": "4 cilindros turbo",
            "transmission": "Automática DSG 7 velocidades",
            "fuel_type": "Nafta",
            "doors": 5,
            "seats": 5,
            "max_speed": 250,
            "acceleration": 6.2,
            "horsepower": 245,
            "torque": 370,
            "weight": 1470,
            "length": 4.28,
            "width": 1.79,
            "description": "El hot hatch por excelencia, pura diversión",
            "image_url": "vw_golf_gti_red.jpg",
            "paymenth_method": "Efectivo"
        },
        {
            "brand": "Mazda",
            "model": "CX-5",
            "year": 2022,
            "color": "Rojo",
            "price": 35000.00,
            "is_available": True,
            "mileage": 18000,
            "engine_type": "4 cilindros SKYACTIV-G",
            "transmission": "Automática 6 velocidades",
            "fuel_type": "Nafta",
            "doors": 5,
            "seats": 5,
            "max_speed": 190,
            "acceleration": 8.7,
            "horsepower": 187,
            "torque": 252,
            "weight": 1620,
            "length": 4.55,
            "width": 1.84,
            "description": "SUV con diseño KODO y tecnología i-ACTIVSENSE",
            "image_url": "mazda_cx5_red.jpg",
            "paymenth_method": "Financiado"
        },
        {
            "brand": "Nissan",
            "model": "Sentra",
            "year": 2020,
            "color": "Azul",
            "price": 16500.00,
            "is_available": True,
            "mileage": 48000,
            "engine_type": "4 cilindros",
            "transmission": "Automática CVT Xtronic",
            "fuel_type": "Nafta",
            "doors": 4,
            "seats": 5,
            "max_speed": 175,
            "acceleration": 10.2,
            "horsepower": 149,
            "torque": 198,
            "weight": 1330,
            "length": 4.64,
            "width": 1.82,
            "description": "Sedán espacioso y confortable para la familia",
            "image_url": "nissan_sentra_blue.jpg",
            "paymenth_method": "Efectivo"
        },
        {
            "brand": "Hyundai",
            "model": "Tucson",
            "year": 2021,
            "color": "Verde",
            "price": 29000.00,
            "is_available": False,
            "mileage": 32000,
            "engine_type": "4 cilindros turbo",
            "transmission": "Automática 8 velocidades",
            "fuel_type": "Nafta",
            "doors": 5,
            "seats": 5,
            "max_speed": 195,
            "acceleration": 8.5,
            "horsepower": 180,
            "torque": 265,
            "weight": 1685,
            "length": 4.50,
            "width": 1.86,
            "description": "SUV moderna con diseño vanguardista",
            "image_url": "hyundai_tucson_green.jpg",
            "paymenth_method": "Financiado"
        }
    ]
    
    inserted_count = 0
    for car in cars:
        # Verificar si el auto ya existe (por marca, modelo y año)
        existing_car = cars_collection.find_one({
            "brand": car["brand"],
            "model": car["model"],
            "year": car["year"]
        })
        if not existing_car:
            cars_collection.insert_one(car)
            inserted_count += 1
            print(f"✓ Auto creado: {car['brand']} {car['model']} {car['year']}")
        else:
            print(f"⊘ Auto ya existe: {car['brand']} {car['model']} {car['year']}")
    
    print(f"\n{inserted_count} autos nuevos creados.")
    return inserted_count

def seed_car_history():
    """Crea historial de interacciones de usuarios con autos"""
    db = get_database()
    cars_history_collection = db["cars_history"]
    users_collection = db["users"]
    cars_collection = db["cars"]
    
    # Obtener usuarios y autos existentes
    users = list(users_collection.find({"is_admin": False}))
    cars = list(cars_collection.find())
    
    if not users or not cars:
        print("⚠ No hay usuarios o autos para crear historial")
        return 0
    
    interactions = [
        {
            "username": "pmarotta",
            "car_models": ["Corolla", "Civic", "Golf GTI"],
            "interaction_type": "view"
        },
        {
            "username": "jperez",
            "car_models": ["BMW X3", "Mercedes-Benz C-Class"],
            "interaction_type": "like"
        },
        {
            "username": "mgarcia",
            "car_models": ["Mazda CX-5", "Hyundai Tucson", "Nissan Sentra"],
            "interaction_type": "view"
        }
    ]
    
    inserted_count = 0
    for interaction in interactions:
        user = users_collection.find_one({"username": interaction["username"]})
        if not user:
            continue
            
        for model_name in interaction["car_models"]:
            car = cars_collection.find_one({"model": model_name})
            if car:
                history_entry = {
                    "username": interaction["username"],
                    "car_id": str(car["_id"]),
                    "interaction_type": interaction["interaction_type"],
                    "timestamp": datetime.utcnow(),
                    "brand": car["brand"],
                    "model": car["model"]
                }
                
                # Verificar si ya existe esta interacción
                existing = cars_history_collection.find_one({
                    "username": history_entry["username"],
                    "car_id": history_entry["car_id"],
                    "interaction_type": history_entry["interaction_type"]
                })
                
                if not existing:
                    cars_history_collection.insert_one(history_entry)
                    inserted_count += 1
                    print(f"✓ Historial creado: {interaction['username']} - {car['brand']} {car['model']}")
    
    print(f"\n{inserted_count} entradas de historial creadas.")
    return inserted_count

def main():
    """Función principal para ejecutar el seed"""
    print("=" * 60)
    print("SEED DE BASE DE DATOS - CONCESIONARIO")
    print("=" * 60)
    print()
    
    try:
        # Seed de usuarios
        print("📝 Creando usuarios...")
        print("-" * 60)
        users_count = seed_users()
        
        print("\n" + "=" * 60)
        
        # Seed de autos
        print("🚗 Creando autos...")
        print("-" * 60)
        cars_count = seed_cars()
        
        print("\n" + "=" * 60)
        
        # Seed de historial
        print("📊 Creando historial de interacciones...")
        print("-" * 60)
        history_count = seed_car_history()
        
        print("\n" + "=" * 60)
        print("✅ SEED COMPLETADO")
        print("=" * 60)
        print(f"Resumen:")
        print(f"  - Usuarios nuevos: {users_count}")
        print(f"  - Autos nuevos: {cars_count}")
        print(f"  - Historial nuevo: {history_count}")
        print()
        print("Credenciales de prueba:")
        print("  Admin: admin / admin123")
        print("  Usuario: pmarotta / password123")
        print("  Usuario: jperez / password123")
        print("  Usuario: mgarcia / password123")
        print("  Admin: lrodriguez / password123")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error durante el seed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
