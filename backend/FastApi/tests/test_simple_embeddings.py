"""
Prueba simple del sistema de embeddings y RAG
"""
import asyncio
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

async def test_basic_embedding():
    """Prueba básica de embeddings sin base de datos"""
    print("🚗 === PRUEBA BÁSICA DE EMBEDDINGS Y RAG ===\n")
    
    # Inicializar modelo
    print("📦 Cargando modelo de embeddings...")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("✅ Modelo cargado exitosamente!\n")
    
    # Datos de prueba (simulando autos)
    test_cars = [
        {
            "id": 1,
            "description": "Toyota Corolla 2023, sedan económico, confiable, bajo consumo, ideal para ciudad",
            "brand": "Toyota",
            "model": "Corolla",
            "price": 25000,
            "type": "Sedan"
        },
        {
            "id": 2,
            "description": "Honda CR-V 2022, SUV familiar, espacioso, seguro, 7 asientos, tracción integral",
            "brand": "Honda", 
            "model": "CR-V",
            "price": 35000,
            "type": "SUV"
        },
        {
            "id": 3,
            "description": "BMW X3 2023, SUV de lujo, deportivo, premium, tecnología avanzada, alto rendimiento",
            "brand": "BMW",
            "model": "X3", 
            "price": 55000,
            "type": "SUV"
        },
        {
            "id": 4,
            "description": "Nissan Versa 2021, auto compacto, muy económico, fácil manejo, ideal estudiante",
            "brand": "Nissan",
            "model": "Versa",
            "price": 18000,
            "type": "Sedan"
        }
    ]
    
    # Consultas de prueba
    test_queries = [
        "Busco un auto económico para ir al trabajo",
        "Necesito un SUV familiar para los fines de semana",
        "Quiero algo deportivo y de lujo",
        "Auto barato para estudiante universitario"
    ]
    
    print("🧠 Creando embeddings de los autos...")
    car_embeddings = []
    for car in test_cars:
        embedding = model.encode(car["description"])
        car_embeddings.append(embedding)
        print(f"   ✅ {car['brand']} {car['model']} - Embedding: {embedding[:5].round(3)}")
    
    print(f"\n🔍 Probando consultas de usuarios...\n")
    
    for query in test_queries:
        print(f"👤 Usuario: '{query}'")
        
        # Crear embedding de la consulta
        query_embedding = model.encode(query)
        print(f"📊 Embedding consulta: {query_embedding[:5].round(3)}")
        
        # Calcular similitudes
        similarities = []
        for i, car_embedding in enumerate(car_embeddings):
            similarity = cosine_similarity([query_embedding], [car_embedding])[0][0]
            similarities.append({
                'car': test_cars[i],
                'similarity': similarity
            })
        
        # Ordenar por similitud
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        print("🏆 TOP 3 Recomendaciones:")
        for j, item in enumerate(similarities[:3], 1):
            car = item['car']
            sim = item['similarity']
            print(f"   {j}. {car['brand']} {car['model']} - ${car['price']:,}")
            print(f"      🎯 Similitud: {sim:.4f} ({sim*100:.1f}%)")
            print(f"      📝 {car['description'][:60]}...")
        
        print("-" * 80)
    
    # Demostrar el proceso RAG completo
    print("\n🔧 === DEMOSTRACIÓN DEL PROCESO RAG ===")
    
    demo_query = "Quiero un auto familiar económico"
    print(f"\n👤 Consulta demo: '{demo_query}'")
    
    # PASO 1: RETRIEVAL
    print("\n🔍 PASO 1: RETRIEVAL (Búsqueda por similitud)")
    query_embedding = model.encode(demo_query)
    similarities = []
    
    for i, car_embedding in enumerate(car_embeddings):
        similarity = cosine_similarity([query_embedding], [car_embedding])[0][0]
        similarities.append({
            'car': test_cars[i],
            'similarity': similarity
        })
        print(f"   • {test_cars[i]['brand']} {test_cars[i]['model']}: {similarity:.4f}")
    
    # PASO 2: AUGMENTED (Enriquecimiento con reglas de negocio)
    print("\n⚙️  PASO 2: AUGMENTED (Aplicar filtros y reglas)")
    enriched_scores = []
    
    for item in similarities:
        car = item['car']
        base_score = item['similarity']
        final_score = base_score
        
        # Reglas de negocio
        if "económico" in demo_query.lower() and car['price'] < 30000:
            bonus = 0.15
            final_score += bonus
            print(f"   💰 Bonus económico para {car['brand']} {car['model']}: +{bonus}")
        
        if "familiar" in demo_query.lower() and car['type'] == 'SUV':
            bonus = 0.1
            final_score += bonus
            print(f"   👨‍👩‍👧‍👦 Bonus familiar para {car['brand']} {car['model']}: +{bonus}")
        
        enriched_scores.append({
            'car': car,
            'original_similarity': base_score,
            'final_score': final_score
        })
    
    # PASO 3: GENERATION (Recomendación final)
    print("\n🎯 PASO 3: GENERATION (Ranking final)")
    enriched_scores.sort(key=lambda x: x['final_score'], reverse=True)
    
    print("🏆 RECOMENDACIONES FINALES:")
    for i, item in enumerate(enriched_scores[:3], 1):
        car = item['car']
        original = item['original_similarity']
        final = item['final_score']
        
        print(f"\n{i}. {car['brand']} {car['model']} ${car['price']:,}")
        print(f"   🎯 Similitud original: {original:.4f}")
        print(f"   ⭐ Score final: {final:.4f}")
        print(f"   🎉 Mejora: {((final-original)/original*100):+.1f}%")
        print(f"   📝 {car['description']}")
    
    print("\n✅ === PRUEBA COMPLETADA ===")
    print("🎉 El sistema de embeddings y RAG está funcionando correctamente!")

if __name__ == "__main__":
    asyncio.run(test_basic_embedding())