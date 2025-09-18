from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import car_router, jwt_auth_router, users_db, carhistory_router, upload_router
from endpoints.chatbot import router as chatbot_router
from endpoints.recommendations import router as recommendations_router

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(car_router.router)
app.include_router(jwt_auth_router.router)
app.include_router(users_db.router)
app.include_router(carhistory_router.router)
app.include_router(upload_router.router)
app.include_router(chatbot_router)
app.include_router(recommendations_router)

@app.get("/")
async def root():
    return {"message": "API del Concesionario Virtual funcionando correctamente"}
