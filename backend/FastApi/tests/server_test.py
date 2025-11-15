"""
Servidor de prueba simplificado para recomendaciones
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints.recommendations import router as recommendations_router

app = FastAPI(title="Concesionario API", description="Sistema de recomendaciones con RAG")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción usar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router de recomendaciones
app.include_router(recommendations_router)

@app.get("/")
async def root():
    return {
        "message": "🚗 API del Concesionario Virtual funcionando correctamente",
        "features": [
            "Recomendaciones con embeddings",
            "Sistema RAG (Retrieval-Augmented Generation)",
            "Análisis semántico en español",
            "Similitud coseno para matching"
        ],
        "endpoints": {
            "quick_recommendations": "/api/recommendations/quick",
            "demo_rag": "/api/recommendations/demo",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "embeddings_ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)