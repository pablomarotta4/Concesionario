# 🌱 Seed de Base de Datos - Concesionario

Script para inicializar la base de datos MongoDB con datos de prueba para desarrollo y testing.

## 📋 Contenido del Seed

### 👥 Usuarios (5)

| Username | Email | Password | Admin |
|----------|-------|----------|-------|
| admin | admin@concesionario.com | admin123 | ✅ |
| pmarotta | pablo@example.com | password123 | ❌ |
| jperez | juan.perez@example.com | password123 | ❌ |
| mgarcia | maria.garcia@example.com | password123 | ❌ |
| lrodriguez | luis.rodriguez@example.com | password123 | ✅ |

### 🚗 Autos (10)

- **Toyota Corolla 2020** - $18,500 (Plateado)
- **Honda Civic 2019** - $17,800 (Negro)
- **BMW X3 2021** - $45,000 (Azul)
- **Mercedes-Benz C-Class 2022** - $52,000 (Negro)
- **Audi A4 2020** - $38,000 (Gris)
- **Ford Focus 2019** - $14,500 (Blanco)
- **Volkswagen Golf GTI 2021** - $32,000 (Rojo)
- **Mazda CX-5 2022** - $35,000 (Rojo)
- **Nissan Sentra 2020** - $16,500 (Azul)
- **Hyundai Tucson 2021** - $29,000 (Verde) - ⚠️ No disponible

### 📊 Historial de Interacciones

- Usuario `pmarotta`: Vistas en Corolla, Civic, Golf GTI
- Usuario `jperez`: Likes en BMW X3 y Mercedes-Benz C-Class
- Usuario `mgarcia`: Vistas en Mazda CX-5, Hyundai Tucson, Nissan Sentra

## 🚀 Ejecución

### Con Docker (Recomendado)

```bash
# Asegúrate de que los servicios estén corriendo
make up

# Ejecutar el seed
make seed
```

### Local (Sin Docker)

```bash
# Desde la raíz del proyecto
make seed-local

# O manualmente
cd Concesionario/backend/FastApi
python seed_database.py
```

### Directamente en Python

```bash
# Desde Concesionario/backend/FastApi
python seed_database.py
```

## ⚙️ Requisitos

### Para ejecución con Docker:
- Docker y Docker Compose corriendo
- Servicios levantados con `make up`

### Para ejecución local:
- Python 3.8+
- MongoDB corriendo en `localhost:27017`
- Dependencias instaladas: `pip install -r requirements.txt`

## 🔧 Variables de Entorno

El script respeta las siguientes variables de entorno:

- `MONGODB_URL`: URL de conexión a MongoDB (default: `mongodb://localhost:27017/`)
- `MONGODB_DATABASE`: Nombre de la base de datos (default: `concesionario`)

## 📝 Características

- ✅ **Idempotente**: Puede ejecutarse múltiples veces sin duplicar datos
- ✅ **Verificación**: Comprueba si los datos ya existen antes de insertar
- ✅ **Contraseñas encriptadas**: Usa bcrypt para hashear contraseñas
- ✅ **Datos realistas**: Información completa y coherente de autos
- ✅ **Feedback visual**: Muestra progreso con emojis y mensajes claros

## 🎯 Salida Esperada

```
============================================================
SEED DE BASE DE DATOS - CONCESIONARIO
============================================================

📝 Creando usuarios...
------------------------------------------------------------
✓ Usuario creado: admin (admin@concesionario.com)
✓ Usuario creado: pmarotta (pablo@example.com)
✓ Usuario creado: jperez (juan.perez@example.com)
✓ Usuario creado: mgarcia (maria.garcia@example.com)
✓ Usuario creado: lrodriguez (luis.rodriguez@example.com)

5 usuarios nuevos creados.

============================================================
🚗 Creando autos...
------------------------------------------------------------
✓ Auto creado: Toyota Corolla 2020
✓ Auto creado: Honda Civic 2019
...
10 autos nuevos creados.

============================================================
📊 Creando historial de interacciones...
------------------------------------------------------------
✓ Historial creado: pmarotta - Toyota Corolla
...
8 entradas de historial creadas.

============================================================
✅ SEED COMPLETADO
============================================================
Resumen:
  - Usuarios nuevos: 5
  - Autos nuevos: 10
  - Historial nuevo: 8

Credenciales de prueba:
  Admin: admin / admin123
  Usuario: pmarotta / password123
  Usuario: jperez / password123
  Usuario: mgarcia / password123
  Admin: lrodriguez / password123
============================================================
```

## 🗑️ Limpiar Datos

Si quieres eliminar todos los datos y volver a ejecutar el seed:

### Opción 1: MongoDB Shell
```bash
# Conectarse a MongoDB
make shell-mongodb

# Dentro de mongosh
use concesionario
db.users.deleteMany({})
db.cars.deleteMany({})
db.cars_history.deleteMany({})
```

### Opción 2: Eliminar volúmenes de Docker
```bash
# Esto eliminará TODOS los datos de MongoDB
make clean
make up
make seed
```

## 🛠️ Personalización

Para modificar los datos del seed, edita el archivo:
```
Concesionario/backend/FastApi/seed_database.py
```

Puedes:
- Agregar más usuarios en la lista `users` de `seed_users()`
- Agregar más autos en la lista `cars` de `seed_cars()`
- Crear más interacciones en `seed_car_history()`

## 🧪 Testing

Para probar que el seed funcionó correctamente:

```bash
# Listar usuarios
make shell-mongodb
> use concesionario
> db.users.find().pretty()

# Listar autos
> db.cars.find().pretty()

# O usar la API
curl http://localhost:8000/cars
curl http://localhost:8000/users
```

## 🔍 Troubleshooting

### Error: "No module named 'passlib'"
```bash
# Instalar dependencias
docker-compose exec backend pip install -r requirements.txt
# o localmente
pip install -r requirements.txt
```

### Error: "pymongo.errors.ServerSelectionTimeoutError"
- Verifica que MongoDB esté corriendo: `docker-compose ps mongodb`
- Verifica la variable `MONGODB_URL` en el archivo `.env`

### Los datos ya existen
- El script es idempotente, mostrará "⊘ Ya existe" para datos duplicados
- Si quieres recrear los datos, elimínalos primero (ver sección "Limpiar Datos")

## 📚 Referencias

- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Passlib Documentation](https://passlib.readthedocs.io/)
- [MongoDB Manual](https://docs.mongodb.com/)
