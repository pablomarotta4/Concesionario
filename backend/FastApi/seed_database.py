"""
Script de seed para inicializar la base de datos con datos de prueba
Ejecutar desde backend/FastApi: python seed_database.py
O usar: make seed (con Docker) o make seed-local (sin Docker)
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt
import os
from datetime import datetime

# Configuración de la base de datos
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGODB_DATABASE", "concesionario")

# Cliente de MongoDB
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


async def seed_users():
    """Crea usuarios de prueba"""
    print("\n📝 Creando usuarios...")
    print("-" * 60)
    
    users = [
        {
            "username": "admin",
            "email": "admin@concesionario.com",
            "full_name": "Administrador",
            "hashed_password": hash_password("admin123"),
            "disabled": False,
            "is_admin": True
        },
        {
            "username": "pmarotta",
            "email": "pablo@example.com",
            "full_name": "Pablo Marotta",
            "hashed_password": hash_password("password123"),
            "disabled": False,
            "is_admin": False
        },
        {
            "username": "jperez",
            "email": "juan.perez@example.com",
            "full_name": "Juan Pérez",
            "hashed_password": hash_password("password123"),
            "disabled": False,
            "is_admin": False
        },
        {
            "username": "mgarcia",
            "email": "maria.garcia@example.com",
            "full_name": "María García",
            "hashed_password": hash_password("password123"),
            "disabled": False,
            "is_admin": False
        },
        {
            "username": "lrodriguez",
            "email": "luis.rodriguez@example.com",
            "full_name": "Luis Rodríguez",
            "hashed_password": hash_password("password123"),
            "disabled": False,
            "is_admin": True
        }
    ]
    
    new_count = 0
    for user in users:
        existing = await db.users.find_one({"username": user["username"]})
        if not existing:
            await db.users.insert_one(user)
            print(f"✓ Usuario creado: {user['username']} ({user['email']})")
            new_count += 1
        else:
            print(f"○ Usuario ya existe: {user['username']}")
    
    print(f"\n{new_count} usuarios nuevos creados.")
    return new_count


async def seed_cars():
    """Crea autos de prueba"""
    print("\n" + "="*60)
    print("🚗 Creando autos...")
    print("-" * 60)
    
    cars = [
        {
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "price": 18500,
            "mileage": 35000,
            "color": "Plateado",
            "fuel_type": "Nafta",
            "transmission": "Automática",
            "engine": "1.8L 4 cilindros",
            "doors": 4,
            "seats": 5,
            "description": "Sedán compacto confiable y eficiente en combustible",
            "features": ["Control de crucero", "Bluetooth", "Cámara trasera"],
            "image_url": "/static/img/toyota-corolla.jpg",
            "available": True
        },
        {
            "brand": "Honda",
            "model": "Civic",
            "year": 2019,
            "price": 17800,
            "mileage": 42000,
            "color": "Negro",
            "fuel_type": "Nafta",
            "transmission": "Manual",
            "engine": "2.0L 4 cilindros",
            "doors": 4,
            "seats": 5,
            "description": "Deportivo y confiable, ideal para ciudad",
            "features": ["Sistema de audio premium", "Apple CarPlay", "Llantas deportivas"],
            "image_url": "/static/img/honda-civic.jpg",
            "available": True
        },
        {
            "brand": "BMW",
            "model": "X3",
            "year": 2021,
            "price": 45000,
            "mileage": 18000,
            "color": "Azul",
            "fuel_type": "Diesel",
            "transmission": "Automática",
            "engine": "2.0L Turbo 4 cilindros",
            "doors": 5,
            "seats": 5,
            "description": "SUV de lujo con tecnología avanzada",
            "features": ["Tracción 4x4", "Techo panorámico", "Sistema de navegación"],
            "image_url": "/static/img/bmw-x3.jpg",
            "available": True
        },
        {
            "brand": "Mercedes-Benz",
            "model": "C-Class",
            "year": 2022,
            "price": 52000,
            "mileage": 8000,
            "color": "Negro",
            "fuel_type": "Nafta",
            "transmission": "Automática",
            "engine": "2.0L Turbo 4 cilindros",
            "doors": 4,
            "seats": 5,
            "description": "Sedán de lujo con prestaciones deportivas",
            "features": ["Asientos de cuero", "Sistema de sonido Burmester", "Asistente de conducción"],
            "image_url": "/static/img/mercedes-c-class.jpg",
            "available": True
        },
        {
            "brand": "Audi",
            "model": "A4",
            "year": 2020,
            "price": 38000,
            "mileage": 25000,
            "color": "Gris",
            "fuel_type": "Nafta",
            "transmission": "Automática",
            "engine": "2.0L TFSI",
            "doors": 4,
            "seats": 5,
            "description": "Sedán elegante con tecnología Quattro",
            "features": ["Tracción integral", "Virtual Cockpit", "Faros LED"],
            "image_url": "/static/img/audi-a4.jpg",
            "available": True
        },
        {
            "brand": "Ford",
            "model": "Focus",
            "year": 2019,
            "price": 14500,
            "mileage": 55000,
            "color": "Blanco",
            "fuel_type": "Nafta",
            "transmission": "Manual",
            "engine": "1.6L 4 cilindros",
            "doors": 5,
            "seats": 5,
            "description": "Hatchback práctico y económico",
            "features": ["Bluetooth", "Control de estabilidad", "Airbags múltiples"],
            "image_url": "/static/img/ford-focus.jpg",
            "available": True
        },
        {
            "brand": "Volkswagen",
            "model": "Golf GTI",
            "year": 2021,
            "price": 32000,
            "mileage": 15000,
            "color": "Rojo",
            "fuel_type": "Nafta",
            "transmission": "Automática DSG",
            "engine": "2.0L TSI Turbo",
            "doors": 5,
            "seats": 5,
            "description": "Hot hatch con rendimiento deportivo",
            "features": ["Modo deportivo", "Asientos deportivos", "Sistema de escape deportivo"],
            "image_url": "/static/img/vw-golf-gti.jpg",
            "available": True
        },
        {
            "brand": "Mazda",
            "model": "CX-5",
            "year": 2022,
            "price": 35000,
            "mileage": 12000,
            "color": "Rojo",
            "fuel_type": "Nafta",
            "transmission": "Automática",
            "engine": "2.5L 4 cilindros",
            "doors": 5,
            "seats": 5,
            "description": "SUV compacto con diseño Kodo",
            "features": ["Tracción AWD", "Head-up display", "Asientos de cuero"],
            "image_url": "/static/img/mazda-cx5.jpg",
            "available": True
        },
        {
            "brand": "Nissan",
            "model": "Sentra",
            "year": 2020,
            "price": 16500,
            "mileage": 38000,
            "color": "Azul",
            "fuel_type": "Nafta",
            "transmission": "CVT",
            "engine": "1.8L 4 cilindros",
            "doors": 4,
            "seats": 5,
            "description": "Sedán familiar confortable",
            "features": ["Cámara de visión 360°", "Control de crucero adaptativo", "Bluetooth"],
            "image_url": "/static/img/nissan-sentra.jpg",
            "available": True
        },
        {
            "brand": "Hyundai",
            "model": "Tucson",
            "year": 2021,
            "price": 29000,
            "mileage": 22000,
            "color": "Verde",
            "fuel_type": "Diesel",
            "transmission": "Automática",
            "engine": "2.0L CRDi",
            "doors": 5,
            "seats": 5,
            "description": "SUV versátil para toda la familia",
            "features": ["Pantalla táctil 8''", "Android Auto", "Sensores de estacionamiento"],
            "image_url": "/static/img/hyundai-tucson.jpg",
            "available": False  # No disponible para testing
        }
    ]
    
    new_count = 0
    for car in cars:
        existing = await db.cars.find_one({
            "brand": car["brand"],
            "model": car["model"],
            "year": car["year"]
        })
        if not existing:
            await db.cars.insert_one(car)
            print(f"✓ Auto creado: {car['brand']} {car['model']} {car['year']}")
            new_count += 1
        else:
            print(f"○ Auto ya existe: {car['brand']} {car['model']} {car['year']}")
    
    print(f"\n{new_count} autos nuevos creados.")
    return new_count


async def seed_history():
    """Crea historial de interacciones para testing de recomendaciones"""
    print("\n" + "="*60)
    print("📊 Creando historial de interacciones...")
    print("-" * 60)
    
    # Obtener IDs necesarios
    user_pmarotta = await db.users.find_one({"username": "pmarotta"})
    user_jperez = await db.users.find_one({"username": "jperez"})
    user_mgarcia = await db.users.find_one({"username": "mgarcia"})
    
    corolla = await db.cars.find_one({"brand": "Toyota", "model": "Corolla"})
    civic = await db.cars.find_one({"brand": "Honda", "model": "Civic"})
    bmw = await db.cars.find_one({"brand": "BMW", "model": "X3"})
    mercedes = await db.cars.find_one({"brand": "Mercedes-Benz", "model": "C-Class"})
    golf = await db.cars.find_one({"brand": "Volkswagen", "model": "Golf GTI"})
    mazda = await db.cars.find_one({"brand": "Mazda", "model": "CX-5"})
    tucson = await db.cars.find_one({"brand": "Hyundai", "model": "Tucson"})
    nissan = await db.cars.find_one({"brand": "Nissan", "model": "Sentra"})
    
    interactions = []
    
    if user_pmarotta and corolla:
        interactions.append({
            "user_id": str(user_pmarotta["_id"]),
            "car_id": str(corolla["_id"]),
            "interaction_type": "view",
            "timestamp": datetime.utcnow()
        })
    
    if user_pmarotta and civic:
        interactions.append({
            "user_id": str(user_pmarotta["_id"]),
            "car_id": str(civic["_id"]),
            "interaction_type": "view",
            "timestamp": datetime.utcnow()
        })
    
    if user_pmarotta and golf:
        interactions.append({
            "user_id": str(user_pmarotta["_id"]),
            "car_id": str(golf["_id"]),
            "interaction_type": "view",
            "timestamp": datetime.utcnow()
        })
    
    if user_jperez and bmw:
        interactions.append({
            "user_id": str(user_jperez["_id"]),
            "car_id": str(bmw["_id"]),
            "interaction_type": "like",
            "timestamp": datetime.utcnow()
        })
    
    if user_jperez and mercedes:
        interactions.append({
            "user_id": str(user_jperez["_id"]),
            "car_id": str(mercedes["_id"]),
            "interaction_type": "like",
            "timestamp": datetime.utcnow()
        })
    
    if user_mgarcia and mazda:
        interactions.append({
            "user_id": str(user_mgarcia["_id"]),
            "car_id": str(mazda["_id"]),
            "interaction_type": "view",
            "timestamp": datetime.utcnow()
        })
    
    if user_mgarcia and tucson:
        interactions.append({
            "user_id": str(user_mgarcia["_id"]),
            "car_id": str(tucson["_id"]),
            "interaction_type": "view",
            "timestamp": datetime.utcnow()
        })
    
    if user_mgarcia and nissan:
        interactions.append({
            "user_id": str(user_mgarcia["_id"]),
            "car_id": str(nissan["_id"]),
            "interaction_type": "view",
            "timestamp": datetime.utcnow()
        })
    
    new_count = 0
    for interaction in interactions:
        existing = await db.carhistory.find_one({
            "user_id": interaction["user_id"],
            "car_id": interaction["car_id"],
            "interaction_type": interaction["interaction_type"]
        })
        if not existing:
            await db.carhistory.insert_one(interaction)
            new_count += 1
            print(f"✓ Historial creado")
    
    print(f"\n{new_count} entradas de historial creadas.")
    return new_count


async def main():
    """Función principal que ejecuta todo el seed"""
    print("="*60)
    print("SEED DE BASE DE DATOS - CONCESIONARIO")
    print("="*60)
    
    try:
        # Crear usuarios
        users_created = await seed_users()
        
        # Crear autos
        cars_created = await seed_cars()
        
        # Crear historial
        history_created = await seed_history()
        
        # Resumen final
        print("\n" + "="*60)
        print("✅ SEED COMPLETADO")
        print("="*60)
        print("Resumen:")
        print(f"  - Usuarios nuevos: {users_created}")
        print(f"  - Autos nuevos: {cars_created}")
        print(f"  - Historial nuevo: {history_created}")
        print("\nCredenciales de prueba:")
        print("  Admin: admin / admin123")
        print("  Usuario: pmarotta / password123")
        print("  Usuario: jperez / password123")
        print("  Usuario: mgarcia / password123")
        print("  Admin: lrodriguez / password123")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error durante el seed: {e}")
        raise
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())

