from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from models.cars import Car

class CarVectorizer:
    """
    Clase para vectorizar autos y consultas de usuarios.
    
    Conceptos clave:
    - TF-IDF: Term Frequency-Inverse Document Frequency
      Mide la importancia de una palabra en un documento relativo a una colección de documentos
    - Cosine Similarity: Mide qué tan similares son dos vectores (0 = diferentes, 1 = idénticos)
    """
    
    def __init__(self):
        # TfidfVectorizer convierte texto en vectores numéricos
        # max_features=1000: Limita a las 1000 palabras más importantes
        # stop_words='english': Ignora palabras comunes como 'the', 'and', etc.
        # ngram_range=(1,2): Considera palabras individuales y pares de palabras
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
        self.fitted = False
        self.car_vectors = None  # Aquí guardaremos los vectores de los autos
        
    def car_to_text_description(self, car: Dict[str, Any]) -> str:
        """
        Convierte un auto (diccionario) en una descripción textual completa.
        
        ¿Por qué hacemos esto?
        - Combinamos TODAS las características del auto en un solo texto
        - Así el vectorizador puede encontrar patrones en palabras como 'deportivo', 'económico', etc.
        
        Ejemplo:
        Input: {"brand": "Toyota", "model": "Corolla", "year": 2020, "color": "red", "price": 20000}
        Output: "Toyota Corolla 2020 red economic sedan fuel_efficient reliable affordable"
        """
        
        # Información básica
        description = f"{car['brand']} {car['model']} {car['year']} {car['color']}"
        
        # Añadimos tipo de combustible y transmisión
        description += f" {car['fuel_type']} {car['transmission']} {car['engine_type']}"
        
        # Categorías basadas en precio (esto ayuda al modelo a entender "económico" vs "premium")
        if car['price'] < 15000:
            description += " economic affordable budget"
        elif car['price'] < 30000:
            description += " mid_range reasonable"
        else:
            description += " premium luxury expensive"
            
        # Categorías basadas en potencia (deportivo vs familiar)
        if car['horsepower'] > 300:
            description += " sporty powerful performance"
        elif car['horsepower'] > 200:
            description += " dynamic moderate_power"
        else:
            description += " efficient economical"
            
        # Tipo de vehículo basado en puertas y asientos
        if car['doors'] == 2:
            description += " coupe sports_car"
        elif car['seats'] > 5:
            description += " family_car spacious"
        else:
            description += " sedan compact"
            
        # Añadimos la descripción original si existe
        if car.get('description'):
            description += f" {car['description']}"
            
        return description.lower()  # Todo en minúsculas para consistencia
    
    def fit(self, cars: List[Dict[str, Any]]):
        """
        'Entrena' el vectorizador con las descripciones de todos los autos.
        
        ¿Qué hace internamente?
        1. Convierte cada auto en texto usando car_to_text_description()
        2. El TfidfVectorizer aprende qué palabras son importantes
        3. Crea un 'vocabulario' de palabras relevantes
        
        cars: Lista de diccionarios, cada uno representa un auto
        """
        print("🚗 Convirtiendo autos a descripciones textuales...")
        car_descriptions = [self.car_to_text_description(car) for car in cars]
        
        print("🧠 Entrenando el vectorizador TF-IDF...")
        self.vectorizer.fit(car_descriptions)
        
        print("📊 Creando vectores para todos los autos...")
        self.car_vectors = self.vectorizer.transform(car_descriptions)
        
        self.fitted = True
        print(f"✅ Vectorizador entrenado con {len(cars)} autos")
        print(f"📝 Vocabulario aprendido: {len(self.vectorizer.get_feature_names_out())} palabras")
        
    def transform_query(self, user_query: str) -> np.ndarray:
        """
        Convierte la consulta del usuario en un vector.
        
        user_query: Texto del usuario como "Quiero un auto rojo deportivo económico"
        
        Returns: Vector numérico que representa la consulta
        """
        if not self.fitted:
            raise ValueError("❌ Debes entrenar el vectorizador primero con fit()")
            
        # Procesamos la consulta de forma similar a como procesamos los autos
        processed_query = user_query.lower()
        
        # Convertimos el texto en vector
        query_vector = self.vectorizer.transform([processed_query])
        return query_vector
    
    def find_similar_cars(self, user_query: str, top_k: int = 5) -> List[tuple]:
        """
        Encuentra los autos más similares a la consulta del usuario.
        
        ¿Cómo funciona?
        1. Convierte la consulta del usuario en vector
        2. Calcula similitud coseno entre la consulta y todos los autos
        3. Devuelve los top_k más similares
        
        user_query: Consulta del usuario
        top_k: Número de autos a devolver
        
        Returns: Lista de tuplas (índice_auto, similitud_score)
        """
        if not self.fitted:
            raise ValueError("❌ Debes entrenar el vectorizador primero con fit()")
            
        print(f"🔍 Buscando autos similares a: '{user_query}'")
        
        # Convertimos la consulta en vector
        query_vector = self.transform_query(user_query)
        
        # Calculamos similitud coseno entre la consulta y todos los autos
        similarities = cosine_similarity(query_vector, self.car_vectors).flatten()
        
        # Obtenemos los índices de los autos más similares
        top_indices = np.argsort(similarities)[::-1][:top_k]  # [::-1] para orden descendente
        
        # Creamos lista de resultados con índice y score de similitud
        results = [(idx, similarities[idx]) for idx in top_indices]
        
        print(f"✅ Encontrados {len(results)} autos similares")
        for idx, score in results:
            print(f"   Auto {idx}: similitud = {score:.3f}")
            
        return results

# Función auxiliar para probar el vectorizador
def test_vectorizer_with_sample_data():
    """
    Función para probar el vectorizador con datos de ejemplo.
    Útil para entender cómo funciona antes de conectar con la base de datos real.
    """
    # Datos de ejemplo
    sample_cars = [
        {
            "brand": "Toyota", "model": "Corolla", "year": 2020, "color": "red",
            "price": 18000, "horsepower": 139, "doors": 4, "seats": 5,
            "fuel_type": "gasoline", "transmission": "automatic", "engine_type": "4-cylinder",
            "description": "Reliable family sedan with excellent fuel economy"
        },
        {
            "brand": "BMW", "model": "M3", "year": 2021, "color": "blue",
            "price": 65000, "horsepower": 473, "doors": 4, "seats": 5,
            "fuel_type": "gasoline", "transmission": "manual", "engine_type": "6-cylinder",
            "description": "High-performance sports sedan with racing heritage"
        },
        {
            "brand": "Honda", "model": "Civic", "year": 2019, "color": "white",
            "price": 16000, "horsepower": 158, "doors": 4, "seats": 5,
            "fuel_type": "gasoline", "transmission": "automatic", "engine_type": "4-cylinder",
            "description": "Compact and efficient city car"
        }
    ]
    
    # Crear y entrenar vectorizador
    vectorizer = CarVectorizer()
    vectorizer.fit(sample_cars)
    
    # Probar consultas
    test_queries = [
        "Quiero un auto deportivo y potente",
        "Busco algo económico y confiable",
        "Necesito un carro familiar blanco"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Consulta: '{query}'")
        results = vectorizer.find_similar_cars(query, top_k=3)
        
        for idx, score in results:
            car = sample_cars[idx]
            print(f"   → {car['brand']} {car['model']} ({car['year']}) - Similitud: {score:.3f}")

if __name__ == "__main__":
    # Ejecutar prueba
    test_vectorizer_with_sample_data()