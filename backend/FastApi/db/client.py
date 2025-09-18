from pymongo import MongoClient

db_client = MongoClient("mongodb://localhost:27017/")

def get_database(database_name: str = "concesionario"):
    """Obtener una instancia de la base de datos"""
    return db_client[database_name]

