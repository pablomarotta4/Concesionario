from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from datetime import datetime
import uuid

router = APIRouter(prefix="/upload", tags=["File Upload"])

UPLOAD_DIR = "static/img"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/car-image")
async def upload_car_image(file: UploadFile = File(...)):
    """
    Sube una imagen para un carro
    """
    try:
        # Validar tipo de archivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen")
        
        # Generar nombre único para el archivo
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Guardar el archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "message": "Imagen subida exitosamente",
            "filename": unique_filename,
            "url": f"/static/img/{unique_filename}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen: {str(e)}")

@router.get("/car-image/{filename}")
async def get_car_image(filename: str):
    """
    Obtiene una imagen de carro por nombre de archivo
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    return FileResponse(file_path) 