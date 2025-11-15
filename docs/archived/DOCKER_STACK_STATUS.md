# 🎉 Stack Dockerizado - Concesionario

## ✅ Estado Actual

Todos los servicios están **levantados y funcionando**:

- ✅ **Frontend React**: http://localhost:3000
- ✅ **Backend FastAPI**: http://localhost:8000
- ✅ **API Docs (Swagger)**: http://localhost:8000/docs
- ✅ **Backoffice Streamlit**: http://localhost:8501
- ✅ **MongoDB**: mongodb://localhost:27017

## 📊 Estado de los Servicios

```bash
NAME                       STATUS                PORTS
concesionario-backend      Up (healthy)          0.0.0.0:8000->8000/tcp
concesionario-backoffice   Up (healthy)          0.0.0.0:8501->8501/tcp
concesionario-frontend     Up                    0.0.0.0:3000->80/tcp
concesionario-mongodb      Up (healthy)          0.0.0.0:27017->27017/tcp
```

## 💾 Volúmenes Creados

```
concesionario_mongodb_data       - Datos persistentes de MongoDB
concesionario_mongodb_config     - Configuración de MongoDB
concesionario_static_files       - Imágenes subidas por usuarios
concesionario_huggingface_cache  - Cache de modelos ML
```

## 🚀 Comandos Útiles

### Ver Logs

```bash
# Todos los servicios
make logs

# Servicio específico
make logs-backend
make logs-frontend
make logs-backoffice
make logs-mongodb

# Seguir logs en tiempo real
docker-compose logs -f backend
```

### Gestión de Servicios

```bash
# Ver estado
make ps
docker-compose ps

# Reiniciar servicios
make restart
make restart-backend

# Detener todo
make down
docker-compose down

# Levantar de nuevo
make up
docker-compose up -d
```

### Acceso a Contenedores

```bash
# Shell en backend
make shell-backend
docker-compose exec backend /bin/bash

# MongoDB shell
make shell-mongodb
docker-compose exec mongodb mongosh -u admin -p concesionario2024

# Ver archivos estáticos
docker-compose exec backend ls -la /app/static/img
```

### Entrenar Modelo ML

```bash
# Desde Makefile
make train-model

# Manualmente
docker-compose exec backend python chatbot/vector.py
```

### Desarrollo

```bash
# Reconstruir una imagen
docker-compose build backend
docker-compose up -d backend

# Ver logs de construcción
docker-compose build --no-cache backend 2>&1 | tee build.log

# Hot reload está activado en backend y backoffice
# Los cambios se reflejan automáticamente
```

### Limpieza

```bash
# Detener y eliminar volúmenes
make clean

# Limpieza completa (incluye imágenes)
make clean-all

# Limpiar solo contenedores detenidos
docker container prune -f

# Limpiar solo imágenes sin usar
docker image prune -f
```

## 🔍 Verificar Salud del Sistema

```bash
# Health check del backend
curl http://localhost:8000/health | python3 -m json.tool

# Respuesta esperada:
{
    "status": "healthy",
    "service": "Concesionario API",
    "version": "1.0.0",
    "mongodb": "connected"
}

# Verificar frontend
curl -I http://localhost:3000

# Verificar backoffice
curl -I http://localhost:8501
```

## 📝 Probar API

```bash
# Listar autos (endpoint público)
curl http://localhost:8000/cars/ | python3 -m json.tool

# Ver documentación interactiva
open http://localhost:8000/docs

# Crear usuario (ejemplo)
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@test.com", "password": "test123"}'
```

## 🐛 Troubleshooting

### MongoDB no conecta

```bash
# Verificar estado
docker-compose ps mongodb

# Ver logs
docker-compose logs mongodb

# Reiniciar
docker-compose restart mongodb
```

### Backend no levanta

```bash
# Ver logs detallados
docker-compose logs backend --tail=100

# Verificar variables de entorno
docker-compose exec backend env | grep MONGO

# Acceder al contenedor
docker-compose exec backend /bin/bash
python -c "from db.client import db_client; print(db_client.server_info())"
```

### Frontend no muestra contenido

```bash
# Verificar build
docker-compose logs frontend

# Reconstruir
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Modelo ML no se descarga

```bash
# Acceder al backend
docker-compose exec backend /bin/bash

# Descargar manualmente
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Verificar cache
ls -la /root/.cache/huggingface
```

## 📊 Monitoreo

```bash
# Ver uso de recursos
docker stats

# Ver uso de disco
docker system df

# Ver volúmenes
docker volume ls
```

## 🔄 Actualizar Código

```bash
# 1. Hacer cambios en el código
# 2. Reconstruir imagen
docker-compose build backend

# 3. Recrear contenedor
docker-compose up -d --force-recreate backend

# O en un solo comando
docker-compose up -d --build backend
```

## 🌐 Acceder desde Otros Dispositivos

Si quieres acceder desde otro dispositivo en tu red local:

1. Obtener tu IP local: `ifconfig | grep "inet "`
2. Acceder desde otro dispositivo:
   - Frontend: http://TU_IP:3000
   - Backend: http://TU_IP:8000
   - Backoffice: http://TU_IP:8501

## 🔐 Credenciales (Desarrollo)

- **MongoDB**:
  - Usuario: `admin`
  - Password: `concesionario2024`
  - Database: `concesionario`

⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción

## 📚 Documentación

- **API**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **README Principal**: [README_DOCKER.md](./README_DOCKER.md)

---

## 🎯 Quick Reference

```bash
# Setup inicial (solo una vez)
cp .env.example .env
make dev

# Desarrollo diario
make up              # Levantar servicios
make logs-backend    # Ver logs
make down            # Apagar todo

# Limpieza
make clean           # Limpiar volúmenes
make clean-all       # Limpieza completa
```

---

✨ **Todo está funcionando correctamente!** ✨
