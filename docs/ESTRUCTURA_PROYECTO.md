# Estructura del Proyecto - Concesionario

## 📁 Estructura Reorganizada

```
Concesionario/
├── backend/                        # Backend de la aplicación
│   └── FastApi/                   
│       ├── main.py                 # Aplicación principal FastAPI
│       ├── requirements.txt        # Dependencias Python
│       ├── chatbot/                # Módulo de chatbot
│       │   ├── agent.py
│       │   └── vectorizer.py
│       ├── db/                     # Configuración de base de datos
│       │   ├── client.py
│       │   └── schemas/
│       ├── endpoints/              # Endpoints especializados
│       │   ├── chatbot.py
│       │   └── recommendations.py
│       ├── models/                 # Modelos de datos
│       │   ├── cars.py
│       │   ├── users.py
│       │   └── carhistory.py
│       ├── routers/                # Routers de la API
│       │   ├── basic_auth_router.py
│       │   ├── jwt_auth_router.py
│       │   ├── car_router.py
│       │   ├── carhistory_router.py
│       │   ├── user_router.py
│       │   ├── upload_router.py
│       │   └── users_db.py
│       ├── services/               # Lógica de negocio
│       │   ├── auth_service.py
│       │   ├── car_services.py
│       │   ├── carhistory_service.py
│       │   ├── embedding_service.py
│       │   └── user_service.py
│       ├── static/                 # Archivos estáticos
│       │   └── img/
│       ├── tests/                  # ✨ Tests organizados
│       │   ├── __init__.py
│       │   ├── test_api.py
│       │   ├── test_direct.py
│       │   ├── test_recommendations.py
│       │   ├── test_service.py
│       │   ├── test_simple_embeddings.py
│       │   ├── final_test.py
│       │   └── server_test.py
│       ├── seed_database.py        # ✨ Script de seed mejorado
│       └── create_test_user.py     # ✨ Script para crear usuarios
│
├── frontend/                       # Frontend React + TypeScript
│   ├── public/
│   │   ├── index.html
│   │   └── placeholder-car.jpg
│   ├── src/
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   ├── components/             # Componentes React
│   │   │   ├── CarAddModal.tsx
│   │   │   ├── CarEditModal.tsx
│   │   │   ├── ImageUpload.tsx
│   │   │   └── Layout/
│   │   ├── contexts/               # Contextos de React
│   │   │   └── AuthContext.tsx
│   │   ├── pages/                  # Páginas
│   │   │   ├── Admin.tsx
│   │   │   ├── CarDetail.tsx
│   │   │   └── ...
│   │   ├── services/               # Servicios de API
│   │   └── types/                  # Definiciones TypeScript
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── README.md
│
├── backoffice/                     # ✨ Panel de administración
│   └── app.py
│
├── preference_model_best/          # ✨ Modelo ML (único)
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── tokenizer.json
│   ├── vocab.txt
│   ├── 1_Pooling/
│   └── 2_Dense/
│
├── docs/                           # ✨ Documentación organizada
│   ├── README_DOCKER.md            # Instrucciones Docker
│   ├── README_SEED.md              # Guía de seed
│   ├── ESTRUCTURA_PROYECTO.md      # Este archivo
│   └── archived/                   # Documentos históricos
│       ├── LOGIN_FIXES.md
│       ├── PRUEBAS_LOGIN.md
│       ├── RESUMEN_LOGIN_FIXES.md
│       ├── DOCKER_STACK_STATUS.md
│       └── SEED_IMPLEMENTATION.md
│
├── .env                            # Variables de entorno
├── .env.example                    # Ejemplo de configuración
├── .gitignore                      # Archivos ignorados
├── .dockerignore                   # Archivos ignorados por Docker
├── docker-compose.yml              # Configuración Docker
├── Makefile                        # Comandos útiles
└── README.md                       # Documentación principal

```

## 🎯 Cambios Realizados

### ✅ Eliminaciones
- ❌ Carpeta `Concesionario/Concesionario/` duplicada (anidación innecesaria)
- ❌ Modelo `preference_model/` duplicado
- ❌ Carpeta vacía `backend/FastApi/preference_model_best/`
- ❌ Archivos `.DS_Store` (sistema macOS)
- ❌ `package-lock.json` duplicado en raíz

### ✅ Reorganizaciones
- 📂 Tests movidos a `backend/FastApi/tests/`
- 📂 Documentación organizada en `docs/`
- 📂 Docs históricos archivados en `docs/archived/`
- 📂 Scripts permanecen en `backend/FastApi/` para fácil acceso desde Docker

### ✅ Mejoras
- ✨ `.gitignore` ampliado y mejorado
- ✨ Estructura más limpia y profesional
- ✨ Mejor separación de responsabilidades
- ✨ Más fácil de navegar y mantener

## 📝 Notas

### Modelos ML
- Solo se mantiene `preference_model_best/` que es el modelo más actualizado
- Los archivos `.bin` están excluidos del git excepto este modelo

### Tests
- Todos los archivos de test ahora están en `backend/FastApi/tests/`
- Incluye `__init__.py` para imports correctos

### Scripts
- `seed_database.py`: Pobla la BD con datos de ejemplo
- `create_test_user.py`: Crea usuarios de prueba

### Documentación
- Documentos activos en `docs/`
- Documentos históricos en `docs/archived/`
- README principal en la raíz

## 🚀 Uso

### Backend
```bash
cd backend/FastApi
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Docker
```bash
docker-compose up --build
```

### Scripts
```bash
# Poblar base de datos
make seed  # Con Docker
# O
cd backend/FastApi && python seed_database.py  # Localmente

# Crear usuario de prueba
cd backend/FastApi && python create_test_user.py
```
