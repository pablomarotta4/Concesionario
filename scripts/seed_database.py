"""
Script de seed para inicializar la base de datos con datos de prueba
Ejecutar: python seed_database.py
"""

import sys
import os

# Agregar el directorio del backend al path
backend_path = os.path.join(os.path.dirname(__file__), 'Concesionario', 'backend', 'FastApi')
sys.path.insert(0, backend_path)

# Cambiar al directorio del backend para que las importaciones funcionen
os.chdir(backend_path)

# Importar y ejecutar el seed
from seed_database import main

if __name__ == "__main__":
    main()
