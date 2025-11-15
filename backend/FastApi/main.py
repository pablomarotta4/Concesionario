from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os

# Importar routers
from routers.car_router import router as car_router
from routers.user_router import router as user_router
from routers.jwt_auth_router import router as jwt_auth_router
from routers.basic_auth_router import router as basic_auth_router
from routers.carhistory_router import router as carhistory_router
from routers.upload_router import router as upload_router
from endpoints.chatbot import router as chatbot_router
from endpoints.recommendations import router as recommendations_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Concesionario API",
    description="API para sistema de concesionario con recomendaciones ML",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint para verificar el estado del servicio"""
    try:
        # Verificar conexión a MongoDB
        from db.client import db_client
        db_client.server_info()
        mongo_status = "connected"
    except Exception as e:
        mongo_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "service": "Concesionario API",
        "version": "1.0.0",
        "mongodb": mongo_status,
    }

# Incluir routers
app.include_router(car_router)
app.include_router(user_router)
app.include_router(jwt_auth_router)
app.include_router(basic_auth_router)
app.include_router(carhistory_router)
app.include_router(upload_router)
app.include_router(chatbot_router)
app.include_router(recommendations_router)

# Montar archivos estáticos
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido a la API de Concesionario",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
