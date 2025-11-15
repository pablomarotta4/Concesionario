from pymongo import MongoClient
import os

# Obtener URL de MongoDB desde variable de entorno o usar default local
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://localhost:27017/"
)

# Crear cliente de MongoDB
db_client = MongoClient(MONGODB_URL)

def get_database(database_name: str = None):
    """Obtener una instancia de la base de datos"""
    if database_name is None:
        database_name = os.getenv("MONGODB_DATABASE", "concesionario")
    return db_client[database_name]

