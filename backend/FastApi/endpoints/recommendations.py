from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from services.embedding_service import embedding_service
# from services.auth_service import get_current_user

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

# Función temporal para autenticación
async def get_current_user():
    return {"id": "test_user_123", "username": "test_user"}

class UserPreferences(BaseModel):
    max_budget: Optional[float] = None
    min_budget: Optional[float] = None
    preferred_brands: Optional[List[str]] = []
    vehicle_type: Optional[str] = None  # SUV, Sedan, Hatchback, etc.
    main_use: Optional[str] = None  # Familiar, Trabajo, Deportivo, etc.
    important_features: Optional[List[str]] = []  # Económico, Espacioso, Deportivo, etc.
    min_year: Optional[int] = None
    transmission_preference: Optional[str] = None  # Manual, Automática
    fuel_preference: Optional[str] = None  # Gasolina, Diésel, Híbrido, etc.
    lifestyle: Optional[str] = None
    priorities: Optional[str] = None

class RecommendationRequest(BaseModel):
    preferences: UserPreferences
    limit: Optional[int] = 5

class QuickRecommendationRequest(BaseModel):
    query: str
    limit: Optional[int] = 5

@router.post("/personalized")
async def get_personalized_recommendations(
    request: RecommendationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Recomendaciones personalizadas usando embeddings y historial del usuario
    """
    try:
        recommendations = await embedding_service.get_personalized_recommendations(
            user_id=current_user["id"],
            preferences=request.preferences.dict(exclude_none=True),
            limit=request.limit
        )
        
        return {
            "recommendations": recommendations,
            "total_found": len(recommendations),
            "user_id": current_user["id"],
            "preferences": request.preferences.dict(exclude_none=True)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en recomendaciones personalizadas: {str(e)}")

@router.post("/quick")
async def get_quick_recommendations(request: QuickRecommendationRequest):
    """
    Recomendaciones rápidas basadas en consulta de texto libre (sin autenticación)
    """
    try:
        recommendations = await embedding_service.get_quick_recommendations(
            query=request.query,
            limit=request.limit
        )
        
        return {
            "recommendations": recommendations,
            "total_found": len(recommendations),
            "query": request.query
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en recomendaciones rápidas: {str(e)}")

@router.post("/similar/{car_id}")
async def get_similar_cars(car_id: str, limit: int = 5):
    """
    Encontrar autos similares a uno específico usando embeddings
    """
    try:
        from bson import ObjectId
        
        # Obtener el auto de referencia
        cars_collection = embedding_service.db["cars"]
        reference_car = await cars_collection.find_one({"_id": ObjectId(car_id)})
        
        if not reference_car:
            raise HTTPException(status_code=404, detail="Auto no encontrado")
        
        # Crear embedding del auto de referencia
        reference_embedding = embedding_service.create_comprehensive_car_embedding(reference_car)
        
        # Encontrar autos similares
        similar_cars = await embedding_service.find_similar_cars(
            reference_embedding, 
            limit=limit + 1  # +1 porque el mismo auto aparecerá en resultados
        )
        
        # Filtrar el auto de referencia de los resultados
        filtered_results = [
            {"car": car, "similarity": similarity} 
            for car, similarity in similar_cars 
            if str(car.get('_id')) != car_id
        ][:limit]
        
        # Convertir ObjectId a string para el auto de referencia
        reference_car['_id'] = str(reference_car['_id'])
        
        return {
            "reference_car": reference_car,
            "similar_cars": filtered_results,
            "total_found": len(filtered_results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error buscando autos similares: {str(e)}")

@router.post("/demo")
async def demo_embedding_rag(request: QuickRecommendationRequest):
    """
    Endpoint de demostración que muestra cómo funciona el proceso RAG paso a paso
    """
    try:
        # Crear embedding de la consulta
        query_embedding = embedding_service.model.encode(request.query)
        
        # Obtener algunos autos para demostración
        cars_collection = embedding_service.db["cars"]
        cars_cursor = cars_collection.find({"available": True}).limit(10)
        cars = await cars_cursor.to_list(length=None)
        
        if not cars:
            return {"error": "No hay autos disponibles para la demostración"}
        
        # Calcular similitudes
        demo_results = []
        for car in cars:
            car_embedding = embedding_service.create_comprehensive_car_embedding(car)
            from sklearn.metrics.pairwise import cosine_similarity
            similarity_score = float(cosine_similarity([query_embedding], [car_embedding])[0][0])
            
            demo_results.append({
                "car": {
                    "id": str(car["_id"]),
                    "brand": car.get("brand", ""),
                    "model": car.get("model", ""),
                    "year": car.get("year", ""),
                    "price": car.get("price", 0),
                    "type": car.get("type", "")
                },
                "similarity_score": similarity_score,
                "similarity_percentage": f"{similarity_score * 100:.1f}%"
            })
        
        # Ordenar por similitud
        demo_results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return {
            "user_query": request.query,
            "embedding_sample": query_embedding[:10].tolist(),  # Primeros 10 valores del embedding
            "cars_analyzed": len(demo_results),
            "top_matches": demo_results[:request.limit],
            "explanation": {
                "process": "RAG (Retrieval-Augmented Generation)",
                "steps": [
                    "1. RETRIEVAL: Convierte la consulta del usuario a un embedding (vector numérico)",
                    "2. RETRIEVAL: Convierte cada auto de la base de datos a embeddings",
                    "3. RETRIEVAL: Calcula similitud coseno entre consulta y autos",
                    "4. AUGMENTED: Aplica filtros de negocio y reglas contextuales",
                    "5. GENERATION: Ordena y retorna las mejores recomendaciones"
                ]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en demostración RAG: {str(e)}")