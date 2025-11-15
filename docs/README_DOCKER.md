# 🚗 Concesionario - Sistema de Recomendación de Autos con ML

Sistema completo de concesionario con recomendaciones personalizadas usando Machine Learning (Sentence Transformers).

## 📋 Componentes

- **Backend**: FastAPI con Python (ML, MongoDB)
- **Frontend**: React + TypeScript + Tailwind CSS
- **Backoffice**: Streamlit para administración
- **Base de Datos**: MongoDB

## 🚀 Quick Start con Docker

### Prerequisitos

- Docker Desktop instalado
- Docker Compose v2+
- 4GB RAM mínimo
- 10GB espacio en disco

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd Concesionario

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# 3. Levantar todo el stack
make dev
```

¡Listo! Los servicios estarán disponibles en:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Backoffice**: http://localhost:8501
- **MongoDB**: mongodb://localhost:27017

## 🛠️ Comandos Disponibles

### Desarrollo

```bash
make help          # Ver todos los comandos disponibles
make build         # Construir imágenes Docker
make up            # Levantar servicios
make down          # Detener servicios
make logs          # Ver logs de todos los servicios
make restart       # Reiniciar servicios
```

### Logs específicos

```bash
make logs-backend
make logs-frontend
make logs-backoffice
make logs-mongodb
```

### Gestión

```bash
make ps            # Ver estado de servicios
make clean         # Limpiar volúmenes
make clean-all     # Limpieza completa
```

### Interactivo

```bash
make shell-backend    # Acceder al contenedor backend
make shell-mongodb    # Acceder a MongoDB shell
make train-model      # Entrenar modelo ML
```

## 📁 Estructura del Proyecto

```
Concesionario/
├── docker-compose.yml          # Orquestación de servicios
├── Makefile                    # Comandos helper
├── .env.example                # Template de variables
├── Concesionario/
│   ├── backend/
│   │   └── FastApi/
│   │       ├── Dockerfile
│   │       ├── main.py         # Punto de entrada
│   │       ├── requirements.txt
│   │       ├── routers/        # Endpoints REST
│   │       ├── services/       # Lógica de negocio
│   │       ├── models/         # Modelos Pydantic
│   │       ├── db/             # Conexión MongoDB
│   │       ├── chatbot/        # Sistema ML
│   │       └── static/         # Imágenes subidas
│   ├── frontend/
│   │   ├── Dockerfile
│   │   ├── nginx.conf          # Config producción
│   │   ├── src/
│   │   └── public/
│   └── backoffice/
│       ├── Dockerfile
│       └── app.py              # App Streamlit
├── preference_model_best/      # Modelo ML entrenado
└── README.md
```

## 🔧 Configuración

### Variables de Entorno

Edita el archivo `.env`:

```bash
# MongoDB
MONGODB_ROOT_USERNAME=admin
MONGODB_ROOT_PASSWORD=tu-password-segura
MONGODB_DATABASE=concesionario

# JWT para autenticación
SECRET_KEY=tu-clave-secreta-muy-larga
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# URLs
REACT_APP_API_URL=http://localhost:8000
```

### Puertos

- **3000**: Frontend React
- **8000**: Backend FastAPI
- **8501**: Backoffice Streamlit
- **27017**: MongoDB

## 🧠 Sistema de Recomendación ML

El sistema usa **Sentence Transformers** para generar vectores de preferencias del usuario:

### Entrenar el Modelo

```bash
# Opción 1: Desde host
cd Concesionario/backend/FastApi/chatbot
python vector.py

# Opción 2: Dentro del contenedor
make train-model
```

### Usar el Modelo

```python
from chatbot.vector import TrainedPreferenceExtractor

extractor = TrainedPreferenceExtractor('./preference_model_best')
preferences = extractor.extract_preferences("Quiero un auto deportivo")
# Output: {'power_score': 0.85, 'price_score': 0.2, ...}
```

## 📊 API Endpoints

### Autenticación

- `POST /token` - Login y obtener JWT
- `POST /users/` - Crear usuario

### Autos

- `GET /cars/` - Listar todos los autos
- `GET /cars/{id}` - Obtener auto por ID
- `POST /cars/` - Crear nuevo auto
- `PUT /cars/{id}` - Actualizar auto
- `DELETE /cars/{id}` - Eliminar auto

### Recomendaciones ML

- `POST /recommendations/` - Obtener recomendaciones personalizadas
- `POST /chatbot/` - Chat con asistente virtual

### Upload

- `POST /upload/` - Subir imagen de auto

Ver documentación completa en: http://localhost:8000/docs

## 🐳 Docker

### Arquitectura

```
┌─────────────┐      ┌─────────────┐
│  Frontend   │─────▶│   Backend   │
│   (React)   │      │  (FastAPI)  │
└─────────────┘      └──────┬──────┘
                            │
                            ├─────▶ MongoDB
                            │
                            └─────▶ ML Models
```

### Volúmenes

- `mongodb_data`: Datos persistentes de MongoDB
- `static_files`: Imágenes subidas
- `huggingface_cache`: Cache de modelos ML
- `./preference_model_best`: Modelo entrenado

### Redes

Todos los servicios comparten la red `concesionario-network` para comunicación interna.

## 🔍 Troubleshooting

### El backend no se conecta a MongoDB

```bash
# Verificar que MongoDB esté healthy
docker-compose ps

# Ver logs de MongoDB
make logs-mongodb

# Verificar conexión
make shell-mongodb
```

### El modelo ML no se descarga

```bash
# Acceder al contenedor
make shell-backend

# Descargar manualmente
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Frontend no se conecta al backend

Verificar que `REACT_APP_API_URL` en `.env` apunte correctamente:
- Desarrollo: `http://localhost:8000`
- Producción: Tu dominio real

### Reiniciar todo

```bash
make down
make clean
make dev
```

## 📝 Desarrollo

### Hot Reload

Los volúmenes están configurados para desarrollo con hot reload:

- **Backend**: Cambios en código Python se reflejan automáticamente
- **Frontend**: Requiere rebuild (`make build && make restart-frontend`)
- **Backoffice**: Cambios se reflejan automáticamente

### Agregar dependencias

```bash
# Backend
docker-compose exec backend pip install nueva-libreria
# Actualizar requirements.txt

# Frontend
docker-compose exec frontend npm install nueva-libreria
# Actualizar package.json
```

## 🚀 Producción

Para producción, crea `docker-compose.prod.yml`:

```yaml
version: '3.8'
services:
  backend:
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    volumes: []  # Sin volúmenes de código
```

Ejecutar:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📄 Licencia

MIT

## 👥 Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

Hecho con ❤️ usando FastAPI, React y Sentence Transformers
