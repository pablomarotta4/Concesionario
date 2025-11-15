#!/usr/bin/env python3
"""Script para crear usuario de prueba en MongoDB"""

from passlib.context import CryptContext
from pymongo import MongoClient
from datetime import datetime
import os

# Configuración
MONGODB_URL = "mongodb://admin:concesionario2024@localhost:27017/"
DB_NAME = "concesionario_db"

# Contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])

# Datos del usuario de prueba
test_user = {
    "username": "admin",
    "email": "admin@concesionario.com",
    "password": crypt.hash("admin123"),
    "disabled": False,
    "created_at": datetime.utcnow(),
    "updated_at": datetime.utcnow()
}

try:
    # Conectar a MongoDB
    client = MongoClient(MONGODB_URL)
    db = client[DB_NAME]
    users_collection = db["users"]
    
    # Verificar si el usuario ya existe
    existing_user = users_collection.find_one({"username": test_user["username"]})
    
    if existing_user:
        print(f"❌ El usuario '{test_user['username']}' ya existe")
        print(f"   ID: {existing_user['_id']}")
    else:
        # Insertar el usuario
        result = users_collection.insert_one(test_user)
        print(f"✅ Usuario creado exitosamente")
        print(f"   Username: {test_user['username']}")
        print(f"   Email: {test_user['email']}")
        print(f"   Password: admin123")
        print(f"   ID: {result.inserted_id}")
    
    # Mostrar todos los usuarios
    print("\n📋 Usuarios en la base de datos:")
    for user in users_collection.find():
        print(f"   - {user['username']} ({user['email']})")
    
    client.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
