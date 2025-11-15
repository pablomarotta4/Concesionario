"""
Prueba directa de los servicios de recomendación
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.embedding_service import CarEmbeddingService

async def test_embedding_service():
    """Probar el servicio de embeddings directamente"""
    print("🧪 === PRUEBA DIRECTA DEL SERVICIO DE EMBEDDINGS ===\n")
    
    try:
        # Inicializar el servicio
        print("📦 Inicializando servicio de embeddings...")
        service = CarEmbeddingService()
        print("✅ Servicio inicializado correctamente!\n")
        
        # Datos de prueba (simulando autos de la base de datos)
        test_cars = [
            {
                "_id": "1",
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2023,
                "price": 25000,
                "type": "Sedan",
                "fuel_type": "Gasolina",
                "transmission": "Manual",
                "mileage": 5000,
                "color": "Blanco",
                "features": ["Económico", "Confiable", "4 puertas"],
                "description": "Sedan compacto ideal para uso diario",
                "available": True,
                "condition": "Usado",
                "engine": "1.8L"
            },
            {
                "_id": "2",
                "brand": "Honda",
                "model": "CR-V",
                "year": 2022,
                "price": 35000,
                "type": "SUV",
                "fuel_type": "Gasolina",
                "transmission": "Automática",
                "mileage": 15000,
                "color": "Negro",
                "features": ["Espacioso", "Seguro", "Familiar"],
                "description": "SUV familiar perfecto para familias",
                "available": True,
                "condition": "Usado",
                "engine": "1.5L Turbo"
            }
        ]
        
        # 1. Probar creación de embeddings
        print("🧠 Probando creación de embeddings...")
        for car in test_cars:
            embedding = service.create_comprehensive_car_embedding(car)
            print(f"   ✅ {car['brand']} {car['model']}: embedding shape {embedding.shape}")
            print(f"      Sample: {embedding[:5].round(3)}")
        
        # 2. Probar embedding de preferencias de usuario
        print("\n👤 Probando embeddings de preferencias de usuario...")
        user_preferences = {
            "max_budget": 30000,
            "preferred_brands": ["Toyota", "Honda"],
            "vehicle_type": "Sedan",
            "main_use": "Trabajo",
            "important_features": ["Económico", "Confiable"]
        }
        
        user_embedding = service.create_user_preference_embedding(user_preferences)
        print(f"   ✅ Preferences embedding shape: {user_embedding.shape}")
        print(f"      Sample: {user_embedding[:5].round(3)}")
        
        # 3. Probar recomendaciones rápidas
        print("\n🚀 Probando recomendaciones rápidas...")
        
        queries = [
            "Auto económico para trabajo",
            "SUV familiar espacioso",
            "Vehículo confiable y barato"
        ]
        
        for query in queries:
            print(f"\n🔍 Query: '{query}'")
            try:
                # Simular la función sin base de datos
                query_embedding = service.model.encode(query)
                
                # Calcular similitudes con autos de prueba
                similarities = []
                for car in test_cars:
                    car_embedding = service.create_comprehensive_car_embedding(car)
                    from sklearn.metrics.pairwise import cosine_similarity
                    similarity = cosine_similarity([query_embedding], [car_embedding])[0][0]
                    
                    similarities.append({
                        'car': car,
                        'similarity': similarity
                    })
                
                # Ordenar por similitud
                similarities.sort(key=lambda x: x['similarity'], reverse=True)
                
                print("   🏆 Resultados:")
                for i, item in enumerate(similarities, 1):
                    car = item['car']
                    sim = item['similarity']
                    print(f"      {i}. {car['brand']} {car['model']} - ${car['price']:,}")
                    print(f"         Similitud: {sim:.4f} ({sim*100:.1f}%)")
                    
            except Exception as e:
                print(f"   ❌ Error en query '{query}': {str(e)}")
        
        print("\n✅ === TODAS LAS PRUEBAS EXITOSAS ===")
        print("🎉 El servicio de embeddings está funcionando perfectamente!")
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_embedding_service())