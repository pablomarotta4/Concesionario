import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import json
from sklearn.metrics.pairwise import cosine_similarity
from db.client import get_database
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class CarEmbeddingService:
    def __init__(self):
        # Modelo optimizado para español y características de productos
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.db = get_database()
        
        # Diccionario de características importantes para autos
        self.car_features_weight = {
            'brand': 0.25,      # Marca muy importante
            'model': 0.20,      # Modelo importante
            'type': 0.15,       # Tipo de vehículo
            'price': 0.15,      # Precio crucial
            'year': 0.10,       # Año relevante
            'fuel_type': 0.08,  # Tipo de combustible
            'transmission': 0.05, # Transmisión
            'color': 0.02       # Color menos importante
        }

    def create_comprehensive_car_embedding(self, car_data: Dict[str, Any]) -> np.ndarray:
        """
        Crear embedding completo para un auto basado en todas sus características
        """
        # Texto principal del auto
        main_description = self._build_car_description(car_data)
        
        # Características técnicas
        technical_features = self._build_technical_description(car_data)
        
        # Características comerciales
        commercial_features = self._build_commercial_description(car_data)
        
        # Combinar todas las descripciones
        full_description = f"{main_description} {technical_features} {commercial_features}"
        
        return self.model.encode(full_description)

    def _build_car_description(self, car: Dict[str, Any]) -> str:
        """Construir descripción principal del auto"""
        return f"""
        {car.get('brand', '')} {car.get('model', '')} {car.get('year', '')}
        Tipo: {car.get('type', '')}
        Color: {car.get('color', '')}
        Precio: ${car.get('price', 0):,}
        """

    def _build_technical_description(self, car: Dict[str, Any]) -> str:
        """Construir descripción técnica"""
        return f"""
        Motor: {car.get('engine', '')}
        Combustible: {car.get('fuel_type', '')}
        Transmisión: {car.get('transmission', '')}
        Kilometraje: {car.get('mileage', 0)} km
        Cilindros: {car.get('cylinders', '')}
        Potencia: {car.get('horsepower', '')} HP
        """

    def _build_commercial_description(self, car: Dict[str, Any]) -> str:
        """Construir descripción comercial y características especiales"""
        features = car.get('features', [])
        condition = car.get('condition', '')
        description = car.get('description', '')
        
        return f"""
        Condición: {condition}
        Características: {', '.join(features) if features else ''}
        Descripción: {description}
        Disponible: {'Sí' if car.get('available', True) else 'No'}
        """

    def create_user_preference_embedding(self, preferences: Dict[str, Any], user_history: List[Dict] = None) -> np.ndarray:
        """
        Crear embedding para preferencias del usuario, incluyendo historial si está disponible
        """
        # Preferencias explícitas
        explicit_prefs = self._build_explicit_preferences(preferences)
        
        # Preferencias implícitas del historial
        implicit_prefs = ""
        if user_history:
            implicit_prefs = self._build_implicit_preferences(user_history)
        
        # Combinar preferencias
        full_preferences = f"{explicit_prefs} {implicit_prefs}"
        
        return self.model.encode(full_preferences)

    def _build_explicit_preferences(self, preferences: Dict[str, Any]) -> str:
        """Construir texto de preferencias explícitas del usuario"""
        budget_text = ""
        if preferences.get('max_budget'):
            budget_text = f"Presupuesto máximo: ${preferences['max_budget']:,}"
        if preferences.get('min_budget'):
            budget_text += f" mínimo: ${preferences['min_budget']:,}"

        return f"""
        {budget_text}
        Marcas preferidas: {', '.join(preferences.get('preferred_brands', []))}
        Tipo de vehículo deseado: {preferences.get('vehicle_type', '')}
        Uso principal: {preferences.get('main_use', '')}
        Características importantes: {', '.join(preferences.get('important_features', []))}
        Año mínimo deseado: {preferences.get('min_year', '')}
        Transmisión preferida: {preferences.get('transmission_preference', '')}
        Combustible preferido: {preferences.get('fuel_preference', '')}
        Estilo de vida: {preferences.get('lifestyle', '')}
        Prioridades: {preferences.get('priorities', '')}
        """

    def _build_implicit_preferences(self, user_history: List[Dict]) -> str:
        """Extraer preferencias implícitas del historial del usuario"""
        if not user_history:
            return ""
        
        # Analizar patrones en el historial
        viewed_brands = [item.get('brand', '') for item in user_history]
        viewed_types = [item.get('type', '') for item in user_history]
        price_ranges = [item.get('price', 0) for item in user_history if item.get('price')]
        
        avg_price = sum(price_ranges) / len(price_ranges) if price_ranges else 0
        most_viewed_brand = max(set(viewed_brands), key=viewed_brands.count) if viewed_brands else ""
        most_viewed_type = max(set(viewed_types), key=viewed_types.count) if viewed_types else ""
        
        return f"""
        Historial muestra interés en: {most_viewed_brand} {most_viewed_type}
        Rango de precios histórico: ${avg_price:,.0f}
        Marcas consultadas frecuentemente: {', '.join(set(viewed_brands[:5]))}
        """

    async def find_similar_cars(self, 
                               target_embedding: np.ndarray, 
                               filters: Dict[str, Any] = None,
                               limit: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        """
        Encontrar autos similares usando embeddings y filtros opcionales
        """
        cars_collection = self.db["cars"]
        
        # Construir query de MongoDB con filtros
        mongo_filter = {"available": True}
        if filters:
            if filters.get('max_price'):
                mongo_filter['price'] = {'$lte': filters['max_price']}
            if filters.get('min_price'):
                if 'price' in mongo_filter:
                    mongo_filter['price']['$gte'] = filters['min_price']
                else:
                    mongo_filter['price'] = {'$gte': filters['min_price']}
            if filters.get('brands'):
                mongo_filter['brand'] = {'$in': filters['brands']}
            if filters.get('types'):
                mongo_filter['type'] = {'$in': filters['types']}
            if filters.get('min_year'):
                mongo_filter['year'] = {'$gte': filters['min_year']}
        
        # Obtener autos que pasan los filtros básicos
        cars_cursor = cars_collection.find(mongo_filter)
        cars = await cars_cursor.to_list(length=None)
        
        if not cars:
            return []
        
        # Calcular similitudes con embeddings
        similarities = []
        for car in cars:
            car_embedding = self.create_comprehensive_car_embedding(car)
            similarity = cosine_similarity([target_embedding], [car_embedding])[0][0]
            
            # Convertir ObjectId a string para serialización
            car['_id'] = str(car['_id'])
            similarities.append((car, float(similarity)))
        
        # Ordenar por similitud y retornar los mejores
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:limit]

    async def get_personalized_recommendations(self, 
                                             user_id: str, 
                                             preferences: Dict[str, Any],
                                             limit: int = 5) -> List[Dict[str, Any]]:
        """
        Obtener recomendaciones personalizadas para un usuario específico
        """
        try:
            # Obtener historial del usuario
            history_collection = self.db["car_history"]
            user_history_cursor = history_collection.find({"user_id": user_id})
            user_history = await user_history_cursor.to_list(length=None)
            
            # Crear embedding de preferencias del usuario (incluyendo historial)
            user_embedding = self.create_user_preference_embedding(preferences, user_history)
            
            # Crear filtros para MongoDB
            filters = {
                'max_price': preferences.get('max_budget'),
                'min_price': preferences.get('min_budget'),
                'brands': preferences.get('preferred_brands'),
                'types': [preferences.get('vehicle_type')] if preferences.get('vehicle_type') else None,
                'min_year': preferences.get('min_year')
            }
            
            # Filtrar None values
            filters = {k: v for k, v in filters.items() if v is not None}
            
            # Encontrar autos similares
            similar_cars = await self.find_similar_cars(user_embedding, filters, limit * 2)
            
            # Aplicar scoring adicional y diversificación
            scored_recommendations = []
            for car, similarity in similar_cars:
                # Score base de similitud
                final_score = similarity
                
                # Bonus por novedad (autos más recientes)
                year_bonus = (car.get('year', 2000) - 2000) / 24 * 0.1  # Bonus hasta 10%
                final_score += year_bonus
                
                # Penalty por autos ya vistos (evitar repetición)
                if any(hist.get('car_id') == car.get('_id') for hist in user_history):
                    final_score *= 0.8  # Reducir score 20%
                
                car['recommendation_score'] = final_score
                car['similarity_score'] = similarity
                scored_recommendations.append(car)
            
            # Ordenar por score final y retornar
            scored_recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
            return scored_recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error en recomendaciones personalizadas: {str(e)}")
            return []

    async def get_quick_recommendations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Recomendaciones rápidas basadas en una consulta de texto libre
        """
        try:
            # Crear embedding de la consulta
            query_embedding = self.model.encode(query)
            
            # Buscar autos similares sin filtros estrictos
            similar_cars = await self.find_similar_cars(query_embedding, None, limit * 2)
            
            # Aplicar scoring contextual basado en la consulta
            scored_recommendations = []
            for car, similarity in similar_cars:
                final_score = similarity
                
                # Bonus contextual basado en palabras clave en la consulta
                query_lower = query.lower()
                
                if "económico" in query_lower or "barato" in query_lower:
                    if car.get('price', 0) < 30000:
                        final_score += 0.15
                
                if "familiar" in query_lower or "familia" in query_lower:
                    if car.get('type', '').lower() in ['suv', 'minivan']:
                        final_score += 0.12
                
                if "lujo" in query_lower or "premium" in query_lower:
                    if car.get('price', 0) > 40000:
                        final_score += 0.10
                
                if "nuevo" in query_lower or "reciente" in query_lower:
                    if car.get('year', 2000) >= 2022:
                        final_score += 0.08
                
                car['recommendation_score'] = final_score
                car['similarity_score'] = similarity
                scored_recommendations.append(car)
            
            # Ordenar y retornar
            scored_recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
            return scored_recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error en recomendaciones rápidas: {str(e)}")
            return []

    def calculate_car_similarity_matrix(self, cars: List[Dict[str, Any]]) -> np.ndarray:
        """
        Calcular matriz de similitud entre todos los autos (útil para recomendaciones tipo 'otros usuarios también vieron')
        """
        if not cars:
            return np.array([])
        
        # Crear embeddings para todos los autos
        car_embeddings = []
        for car in cars:
            embedding = self.create_comprehensive_car_embedding(car)
            car_embeddings.append(embedding)
        
        # Calcular matriz de similitud
        embeddings_matrix = np.array(car_embeddings)
        similarity_matrix = cosine_similarity(embeddings_matrix)
        
        return similarity_matrix

# Instancia global del servicio
embedding_service = CarEmbeddingService()