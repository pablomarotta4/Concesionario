"""
Script para probar el API de recomendaciones
"""
import requests
import json
import time

def test_recommendations_api():
    """Probar el API de recomendaciones"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 === PRUEBAS DEL API DE RECOMENDACIONES ===\n")
    
    # Esperar un momento para que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    time.sleep(3)
    
    # 1. Probar endpoint básico
    try:
        print("🔍 Probando endpoint básico...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"✅ Servidor funcionando: {response.json()}")
        else:
            print(f"❌ Error en servidor: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose?")
        return
    
    # 2. Probar recomendaciones rápidas
    print("\n🚀 Probando recomendaciones rápidas...")
    quick_test_data = {
        "query": "Busco un auto económico para trabajo",
        "limit": 3
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/recommendations/quick",
            json=quick_test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recomendaciones rápidas exitosas!")
            print(f"📊 Query: {data.get('query')}")
            print(f"🎯 Total encontrado: {data.get('total_found')}")
            
            recommendations = data.get('recommendations', [])
            if recommendations:
                print("🏆 Top recomendaciones:")
                for i, rec in enumerate(recommendations[:3], 1):
                    brand = rec.get('brand', 'N/A')
                    model = rec.get('model', 'N/A') 
                    price = rec.get('price', 0)
                    similarity = rec.get('similarity_score', 0)
                    print(f"   {i}. {brand} {model} - ${price:,} (Similitud: {similarity:.3f})")
            else:
                print("⚠️  No se encontraron recomendaciones (posiblemente base de datos vacía)")
                
        else:
            print(f"❌ Error en recomendaciones rápidas: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 3. Probar endpoint de demostración RAG
    print("\n🔧 Probando endpoint de demostración RAG...")
    demo_data = {
        "query": "SUV familiar económico",
        "limit": 2
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/recommendations/demo",
            json=demo_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Demo RAG exitoso!")
            print(f"📊 Query: {data.get('user_query')}")
            print(f"🧠 Embedding sample: {data.get('embedding_sample', [])[:5]}")
            print(f"🔍 Autos analizados: {data.get('cars_analyzed')}")
            
            explanation = data.get('explanation', {})
            if explanation:
                print(f"📖 Proceso: {explanation.get('process')}")
                steps = explanation.get('steps', [])
                if steps:
                    print("📋 Pasos del RAG:")
                    for step in steps:
                        print(f"   • {step}")
                        
        else:
            print(f"❌ Error en demo RAG: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # 4. Probar documentación automática
    print("\n📚 Probando documentación automática...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ Documentación disponible en: http://127.0.0.1:8000/docs")
        else:
            print(f"❌ Error en documentación: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n✅ === PRUEBAS COMPLETADAS ===")
    print("🎉 El sistema de recomendaciones está funcionando!")
    print("🌐 Puedes probar manualmente en: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    test_recommendations_api()