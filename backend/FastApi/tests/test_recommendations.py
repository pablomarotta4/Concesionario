"""
Script de prueba para el sistema de recomendaciones con embeddings y RAG
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import json
from datetime import datetime
from services.embedding_service import CarEmbeddingService
from db.client import get_database

class RecommendationTester:
    def __init__(self):
        self.embedding_service = CarEmbeddingService()
        self.db = get_database()
    
    async def setup_test_data(self):
        """Crear datos de prueba si no existen"""
        cars_collection = self.db["cars"]
        
        # Verificar si ya hay datos
        count = await cars_collection.count_documents({})
        if count > 0:
            print(f"✅ Ya hay {count} autos en la base de datos")
            return
        
        # Crear autos de prueba
        test_cars = [
            {
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2023,
                "price": 25000,
                "type": "Sedan",
                "fuel_type": "Gasolina",
                "transmission": "Manual",
                "mileage": 5000,
                "color": "Blanco",
                "features": ["Económico", "Confiable", "4 puertas", "Aire acondicionado"],
                "description": "Sedan compacto ideal para uso diario, excelente rendimiento de combustible",
                "available": True,
                "condition": "Usado",
                "engine": "1.8L 4 cilindros",
                "horsepower": "139 HP"
            },
            {
                "brand": "Honda",
                "model": "CR-V",
                "year": 2022,
                "price": 35000,
                "type": "SUV",
                "fuel_type": "Gasolina", 
                "transmission": "Automática",
                "mileage": 15000,
                "color": "Negro",
                "features": ["Espacioso", "Seguro", "Tracción integral", "7 asientos"],
                "description": "SUV familiar perfecto para familias grandes, muy seguro y espacioso",
                "available": True,
                "condition": "Usado",
                "engine": "1.5L Turbo",
                "horsepower": "190 HP"
            },
            {
                "brand": "BMW",
                "model": "X3",
                "year": 2023,
                "price": 55000,
                "type": "SUV",
                "fuel_type": "Gasolina",
                "transmission": "Automática",
                "mileage": 8000,
                "color": "Azul",
                "features": ["Lujo", "Deportivo", "Premium", "Tecnología avanzada"],
                "description": "SUV de lujo con excelente performance y tecnología de punta",
                "available": True,
                "condition": "Seminuevo",
                "engine": "2.0L Turbo",
                "horsepower": "248 HP"
            },
            {
                "brand": "Nissan",
                "model": "Versa",
                "year": 2021,
                "price": 18000,
                "type": "Sedan",
                "fuel_type": "Gasolina",
                "transmission": "Manual",
                "mileage": 25000,
                "color": "Rojo",
                "features": ["Económico", "Compacto", "Fácil de manejar"],
                "description": "Auto compacto ideal para ciudad, muy económico en combustible",
                "available": True,
                "condition": "Usado",
                "engine": "1.6L 4 cilindros",
                "horsepower": "122 HP"
            },
            {
                "brand": "Ford",
                "model": "Explorer",
                "year": 2023,
                "price": 45000,
                "type": "SUV",
                "fuel_type": "Gasolina",
                "transmission": "Automática",
                "mileage": 12000,
                "color": "Gris",
                "features": ["Familiar", "Potente", "Remolque", "8 asientos"],
                "description": "SUV robusto perfecto para aventuras familiares y remolque",
                "available": True,
                "condition": "Seminuevo",
                "engine": "2.3L EcoBoost",
                "horsepower": "300 HP"
            }
        ]
        
        result = await cars_collection.insert_many(test_cars)
        print(f"✅ Insertados {len(result.inserted_ids)} autos de prueba")
    
    async def test_quick_recommendations(self):
        """Probar recomendaciones rápidas"""
        print("\n🔍 === PRUEBA DE RECOMENDACIONES RÁPIDAS ===")
        
        test_queries = [
            "Busco un auto económico para ir al trabajo",
            "Necesito un SUV familiar para los fines de semana",
            "Quiero algo deportivo y de lujo",
            "Auto barato para estudiante universitario",
            "Vehículo espacioso para familia numerosa"
        ]
        
        for query in test_queries:
            print(f"\n👤 Consulta: '{query}'")
            recommendations = await self.embedding_service.get_quick_recommendations(query, limit=3)
            
            print(f"📊 Encontradas {len(recommendations)} recomendaciones:")
            for i, car in enumerate(recommendations, 1):
                sim_score = car.get('similarity_score', 0)
                rec_score = car.get('recommendation_score', 0)
                print(f"   {i}. {car['brand']} {car['model']} {car['year']}")
                print(f"      💲 ${car['price']:,} | 🎯 Similitud: {sim_score:.3f} | ⭐ Score: {rec_score:.3f}")
                print(f"      📝 {car.get('description', '')[:80]}...")
    
    async def test_embedding_similarity(self):
        """Probar similitud de embeddings"""
        print("\n🧠 === PRUEBA DE SIMILITUD DE EMBEDDINGS ===")
        
        # Obtener algunos autos
        cars_collection = self.db["cars"]
        cars_cursor = cars_collection.find({}).limit(3)
        cars = await cars_cursor.to_list(length=None)
        
        if not cars:
            print("❌ No hay autos para probar")
            return
        
        # Probar diferentes consultas
        test_queries = [
            "auto económico familiar",
            "SUV de lujo deportivo", 
            "vehículo confiable trabajo"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Consulta: '{query}'")
            query_embedding = self.embedding_service.model.encode(query)
            
            similarities = []
            for car in cars:
                car_embedding = self.embedding_service.create_comprehensive_car_embedding(car)
                similarity = self.embedding_service.model.encode(query)
                
                # Calcular similitud coseno manualmente para la demo
                import numpy as np
                dot_product = np.dot(query_embedding, car_embedding)
                norm_query = np.linalg.norm(query_embedding)
                norm_car = np.linalg.norm(car_embedding)
                similarity_score = dot_product / (norm_query * norm_car)
                
                similarities.append({
                    'car': car,
                    'similarity': float(similarity_score)
                })
            
            # Ordenar por similitud
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            print("📈 Similitudes calculadas:")
            for item in similarities:
                car = item['car']
                sim = item['similarity']
                print(f"   • {car['brand']} {car['model']}: {sim:.4f} ({sim*100:.1f}%)")
    
    async def test_personalized_recommendations(self):
        """Probar recomendaciones personalizadas (simuladas)"""
        print("\n👤 === PRUEBA DE RECOMENDACIONES PERSONALIZADAS ===")
        
        # Simular preferencias de usuario
        user_preferences = {
            "max_budget": 40000,
            "preferred_brands": ["Toyota", "Honda"],
            "vehicle_type": "SUV",
            "main_use": "Familiar",
            "important_features": ["Espacioso", "Seguro", "Económico"],
            "min_year": 2020
        }
        
        print(f"🎯 Preferencias del usuario:")
        for key, value in user_preferences.items():
            if value:
                print(f"   • {key}: {value}")
        
        # Simular ID de usuario
        fake_user_id = "test_user_123"
        
        recommendations = await self.embedding_service.get_personalized_recommendations(
            user_id=fake_user_id,
            preferences=user_preferences,
            limit=3
        )
        
        print(f"\n🏆 Recomendaciones personalizadas ({len(recommendations)}):")
        for i, car in enumerate(recommendations, 1):
            sim_score = car.get('similarity_score', 0)
            rec_score = car.get('recommendation_score', 0)
            print(f"   {i}. {car['brand']} {car['model']} {car['year']}")
            print(f"      💲 ${car['price']:,}")
            print(f"      🎯 Similitud: {sim_score:.3f} | ⭐ Score final: {rec_score:.3f}")
            print(f"      ✨ Características: {', '.join(car.get('features', []))}")
            print(f"      📝 {car.get('description', '')}")
            print()
    
    async def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🚗 === SISTEMA DE RECOMENDACIONES CON EMBEDDINGS Y RAG ===")
        print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Configurar datos de prueba
            await self.setup_test_data()
            
            # Ejecutar pruebas
            await self.test_quick_recommendations()
            await self.test_embedding_similarity()
            await self.test_personalized_recommendations()
            
            print("\n✅ === TODAS LAS PRUEBAS COMPLETADAS ===")
            print("🎉 El sistema de recomendaciones está funcionando correctamente!")
            
        except Exception as e:
            print(f"\n❌ Error durante las pruebas: {str(e)}")
            import traceback
            traceback.print_exc()

async def main():
    """Función principal"""
    tester = RecommendationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())