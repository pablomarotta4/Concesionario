from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import user_router, car_router, basic_auth_router, jwt_auth_router, users_db, carhistory_router, upload_router


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

app.include_router(car_router.router)
app.include_router(jwt_auth_router.router)
app.include_router(users_db.router)
app.include_router(carhistory_router.router)
app.include_router(upload_router.router)

@app.get("/")
async def root():
    return {"message": "API del Concesionario Virtual funcionando correctamente"}
