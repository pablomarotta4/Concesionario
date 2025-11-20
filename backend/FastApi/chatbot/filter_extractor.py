import logging
from typing import Dict, Any, List, Optional
import os
from chatbot.vector import TrainedPreferenceExtractor
from chatbot.llm_service import get_ollama_service

logger = logging.getLogger(__name__)


class FilterExtractor:
    """
    Extractor de filtros que combina:
    - TrainedPreferenceExtractor (ML) para scores de preferencias
    - LLM (Ollama) para interpretar contexto y generar filtros estructurados
    """
    
    def __init__(self, model_path: str = None):
        # Ruta al modelo entrenado (relativa al directorio del proyecto)
        if model_path is None:
            # Intentar encontrar el modelo en diferentes ubicaciones
            possible_paths = [
                "./preference_model_best",
                "../preference_model_best",
                os.path.join(os.path.dirname(__file__), "../../preference_model_best"),
                os.path.join(os.path.dirname(__file__), "../../../preference_model_best")
            ]
            model_path = "./preference_model_best"
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
        
        self.preference_extractor = TrainedPreferenceExtractor(model_path=model_path)
        self.llm_service = get_ollama_service()
        
        logger.info(f"FilterExtractor inicializado con modelo: {model_path}")
    
    async def extract_filters_from_message(
        self, 
        message: str, 
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Extrae filtros estructurados desde un mensaje en lenguaje natural.
        
        Combina:
        1. Scores de preferencias del modelo ML entrenado
        2. Interpretación contextual del LLM
        3. Mapeo a filtros compatibles con MongoDB
        
        Args:
            message: Mensaje del usuario
            conversation_history: Historial de conversación (opcional)
            
        Returns:
            dict: Filtros estructurados para MongoDB
        """
        try:
            # Paso 1: Obtener scores de preferencias del modelo ML
            ml_preferences = self.preference_extractor.extract_preferences(message)
            logger.info(f"Scores ML: {ml_preferences}")
            
            # Paso 2: Usar LLM para extraer filtros estructurados
            llm_filters = await self.llm_service.extract_filters(
                message, 
                conversation_history
            )
            logger.info(f"Filtros LLM: {llm_filters}")
            
            # Paso 3: Combinar y enriquecer filtros
            combined_filters = self._combine_filters(ml_preferences, llm_filters, message)
            
            logger.info(f"Filtros combinados: {combined_filters}")
            return combined_filters
            
        except Exception as e:
            logger.error(f"Error extrayendo filtros: {e}")
            # Fallback: usar solo scores ML
            return self._ml_scores_to_filters(ml_preferences)
    
    def _combine_filters(
        self, 
        ml_scores: Dict[str, float], 
        llm_filters: Dict[str, Any],
        original_message: str
    ) -> Dict[str, Any]:
        """
        Combina filtros del ML y LLM, priorizando información más específica.
        """
        combined = {}
        
        # Usar filtros del LLM como base (más específicos)
        combined.update(llm_filters)
        
        # Enriquecer con información del ML cuando falta
        # Precio: score alto = precio bajo (económico)
        if "price" not in combined and ml_scores.get("price_score", 0.5) > 0.7:
            # Usuario busca algo económico
            if "price" not in combined:
                combined["price"] = {"max": 30000}  # Precio máximo razonable para económico
        
        # Potencia: score alto = alta potencia
        if "horsepower" not in combined and ml_scores.get("power_score", 0.5) > 0.7:
            combined["horsepower"] = {"min": 200}  # Alta potencia
        elif "horsepower" not in combined and ml_scores.get("power_score", 0.5) < 0.3:
            combined["horsepower"] = {"max": 150}  # Baja potencia
        
        # Tamaño: score alto = grande
        if "size_category" not in combined and ml_scores.get("size_score", 0.5) > 0.7:
            combined["size_category"] = "large"
            if "seats" not in combined:
                combined["seats"] = {"min": 5}
        elif "size_category" not in combined and ml_scores.get("size_score", 0.5) < 0.3:
            combined["size_category"] = "small"
            if "seats" not in combined:
                combined["seats"] = {"max": 4}
        
        # Eficiencia: score alto = híbrido/eléctrico
        if "fuel_type" not in combined and ml_scores.get("efficiency_score", 0.5) > 0.7:
            combined["fuel_type"] = ["Híbrido", "Eléctrico"]
        
        # Marca: score alto = marca premium
        if "brand" not in combined and ml_scores.get("brand_score", 0.5) > 0.7:
            # No especificamos marca, pero el usuario valora marcas premium
            # Esto se puede usar para scoring adicional, no para filtrar
            pass
        
        # Detectar tipo de vehículo desde el mensaje si no está en LLM
        if "type" not in combined:
            message_lower = original_message.lower()
            if any(word in message_lower for word in ["suv", "camioneta", "todoterreno"]):
                combined["type"] = "SUV"
            elif any(word in message_lower for word in ["sedan", "sedán"]):
                combined["type"] = "Sedan"
            elif any(word in message_lower for word in ["hatchback", "compacto"]):
                combined["type"] = "Hatchback"
            elif any(word in message_lower for word in ["pickup"]):
                combined["type"] = "Pickup"
            elif any(word in message_lower for word in ["van", "minivan", "furgoneta"]):
                combined["type"] = "Van"
        
        # Detectar tamaño/espacio desde el mensaje
        message_lower = original_message.lower()
        if any(word in message_lower for word in ["grande", "amplio", "espacioso", "familiar"]):
            # Usuario busca vehículo grande
            if "seats" not in combined:
                combined["seats"] = {"min": 6}  # Al menos 6 asientos para "grande"
            if "size_category" not in combined:
                combined["size_category"] = "large"
        
        # Detectar potencia desde el mensaje
        if any(word in message_lower for word in ["potente", "deportivo", "rápido", "veloz"]):
            # Usuario busca vehículo potente
            if "horsepower" not in combined:
                combined["horsepower"] = {"min": 180}  # Al menos 180 HP para "potente"
        
        # Detectar economía/precio desde el mensaje
        if any(word in message_lower for word in ["económico", "barato", "accesible"]):
            # Usuario busca vehículo económico
            if "price" not in combined:
                combined["price"] = {"max": 25000}
        
        # Detectar lujo desde el mensaje
        if any(word in message_lower for word in ["lujo", "premium", "exclusivo"]):
            # Usuario busca vehículo de lujo
            if "price" not in combined:
                combined["price"] = {"min": 45000}
        
        return combined
    
    def _ml_scores_to_filters(self, ml_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Convierte scores ML a filtros básicos (fallback).
        """
        filters = {}
        
        # Precio
        if ml_scores.get("price_score", 0.5) > 0.7:
            filters["price"] = {"max": 30000}
        
        # Potencia
        if ml_scores.get("power_score", 0.5) > 0.7:
            filters["horsepower"] = {"min": 200}
        elif ml_scores.get("power_score", 0.5) < 0.3:
            filters["horsepower"] = {"max": 150}
        
        # Tamaño
        if ml_scores.get("size_score", 0.5) > 0.7:
            filters["size_category"] = "large"
            filters["seats"] = {"min": 5}
        elif ml_scores.get("size_score", 0.5) < 0.3:
            filters["size_category"] = "small"
            filters["seats"] = {"max": 4}
        
        # Eficiencia
        if ml_scores.get("efficiency_score", 0.5) > 0.7:
            filters["fuel_type"] = ["Híbrido", "Eléctrico"]
        
        return filters
    
    def identify_missing_info(self, filters: Dict[str, Any]) -> List[str]:
        """
        Identifica información faltante importante para hacer preguntas de clarificación.
        
        Args:
            filters: Filtros extraídos
            
        Returns:
            List[str]: Lista de información faltante
        """
        missing = []
        
        # Verificar si hay filtros válidos (no vacíos o con valores por defecto)
        has_valid_price = False
        if "price" in filters:
            price = filters["price"]
            if isinstance(price, dict):
                # Considerar válido si tiene min > 0 o max > 0 y no es un rango muy amplio por defecto
                has_min = "min" in price and price["min"] > 0
                has_max = "max" in price and price["max"] > 0
                # Si max es muy alto (ej: 60000), probablemente es un valor por defecto
                if has_max and price["max"] < 100000:
                    has_valid_price = True
                elif has_min:
                    has_valid_price = True
            elif isinstance(price, (int, float)) and price > 0:
                has_valid_price = True
        
        has_valid_size = False
        if "size_category" in filters and filters["size_category"]:
            has_valid_size = True
        if "seats" in filters:
            seats = filters["seats"]
            if isinstance(seats, dict):
                has_valid_size = ("min" in seats and seats["min"] > 0) or ("max" in seats and seats["max"] > 0)
            elif isinstance(seats, int) and seats > 0:
                has_valid_size = True
        
        # Información crítica que deberíamos tener
        if not has_valid_price:
            missing.append("presupuesto")
        
        if not has_valid_size:
            missing.append("tamaño o número de asientos")
        
        return missing
    
    def validate_filters(self, filters: Dict[str, Any]) -> tuple:
        """
        Valida que los filtros sean coherentes y ejecutables.
        
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        # Validar precio
        if "price" in filters and isinstance(filters["price"], dict):
            if "min" in filters["price"] and "max" in filters["price"]:
                if filters["price"]["min"] > filters["price"]["max"]:
                    return False, "El precio mínimo no puede ser mayor al máximo"
        
        # Validar asientos
        if "seats" in filters and isinstance(filters["seats"], dict):
            if "min" in filters["seats"] and "max" in filters["seats"]:
                if filters["seats"]["min"] > filters["seats"]["max"]:
                    return False, "El número mínimo de asientos no puede ser mayor al máximo"
        
        # Validar potencia
        if "horsepower" in filters and isinstance(filters["horsepower"], dict):
            if "min" in filters["horsepower"] and "max" in filters["horsepower"]:
                if filters["horsepower"]["min"] > filters["horsepower"]["max"]:
                    return False, "La potencia mínima no puede ser mayor a la máxima"
        
        return True, None


# Instancia global del extractor
_filter_extractor: Optional[FilterExtractor] = None


def get_filter_extractor() -> FilterExtractor:
    """Obtiene la instancia global del extractor de filtros (singleton)"""
    global _filter_extractor
    if _filter_extractor is None:
        _filter_extractor = FilterExtractor()
    return _filter_extractor

