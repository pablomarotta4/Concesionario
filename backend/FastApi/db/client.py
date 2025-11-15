from pymongo import MongoClient
import os

# Obtener URL de MongoDB desde variable de entorno o usar default local
MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://admin:changeme123@mongodb:27017/concesionario?authSource=admin"
)

# Crear cliente de MongoDB
db_client = MongoClient(MONGODB_URL)

# Obtener la base de datos por defecto
database_name = os.getenv("MONGODB_DATABASE", "concesionario")

def get_database(db_name: str = None):
    """Obtener una instancia de la base de datos"""
    if db_name is None:
        db_name = database_name
    return db_client[db_name]

# Exponer la base de datos para uso directo
local = db_client[database_name]

