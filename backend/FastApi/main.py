from fastapi import FastAPI
from routers import user_router, car_router


app = FastAPI()

app.include_router(user_router.router)
app.include_router(car_router.router)

@app.get("/")
async def root():
    return {"message": "API del Concesionario Virtual funcionando correctamente"}
