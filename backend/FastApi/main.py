from fastapi import FastAPI
from routers import user_router, car_router, basic_auth_router, jwt_auth_router, users_db


app = FastAPI()

app.include_router(car_router.router)
app.include_router(jwt_auth_router.router)
app.include_router(users_db.router)

@app.get("/")
async def root():
    return {"message": "API del Concesionario Virtual funcionando correctamente"}
