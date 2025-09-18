"""
Prueba directa del endpoint de recomendaciones sin servidor
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from endpoints.recommendations import router
from endpoints.recommendations import QuickRecommendationRequest

async def test_direct_recommendations():
    """Probar el endpoint directamente"""
    print("🧪 === PRUEBA DIRECTA DE RECOMENDACIONES ===\n")
    
    # Crear una solicitud de prueba
    request = QuickRecommendationRequest(
        query="Busco un auto económico para trabajo",
        limit=3
    )
    
    try:
        # Llamar directamente al endpoint
        print(f"🔍 Probando consulta: '{request.query}'")
        result = await router.url_path_for("get_quick_recommendations").__class__(request)
        
        print(f"✅ Resultado obtenido:")
        print(result)
        
    except Exception as e:
        print(f"❌ Error en prueba directa: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_recommendations())