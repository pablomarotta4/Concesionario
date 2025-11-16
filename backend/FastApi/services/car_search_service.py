from typing import List, Dict, Any, Optional
from bson import ObjectId
import logging
from db.client import get_database
from db.schemas.cars import car_schema

logger = logging.getLogger(__name__)


class CarSearchService:
    """
    Servicio para buscar autos en MongoDB usando filtros estructurados.
    Incluye lógica de fallback cuando no hay resultados exactos.
    """
    
    def __init__(self):
        self.db = get_database()
        self.cars_collection = self.db["cars"]
        
        # Mapeo de categorías de tamaño a rangos de asientos y dimensiones
        self.size_mapping = {
            "small": {"seats": {"$lte": 4}, "length": {"$lt": 4.5}},
            "medium": {"seats": {"$gte": 5, "$lte": 6}, "length": {"$gte": 4.5, "$lt": 5.0}},
            "large": {"seats": {"$gte": 7}, "length": {"$gte": 5.0}}
        }
    
    def _build_mongo_query(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Construye una query de MongoDB desde filtros estructurados.
        
        Args:
            filters: Filtros en formato estructurado
            
        Returns:
            dict: Query de MongoDB
        """
        query = {"is_available": True}  # Solo autos disponibles
        
        # Filtro de precio
        if "price" in filters:
            price_filter = filters["price"]
            if isinstance(price_filter, dict):
                if "min" in price_filter:
                    query["price"] = {"$gte": price_filter["min"]}
                if "max" in price_filter:
                    if "price" in query:
                        query["price"]["$lte"] = price_filter["max"]
                    else:
                        query["price"] = {"$lte": price_filter["max"]}
            elif isinstance(price_filter, (int, float)):
                query["price"] = {"$lte": price_filter}
        
        # Filtro de asientos
        if "seats" in filters:
            seats_filter = filters["seats"]
            if isinstance(seats_filter, dict):
                if "min" in seats_filter:
                    query["seats"] = {"$gte": seats_filter["min"]}
                if "max" in seats_filter:
                    if "seats" in query:
                        query["seats"]["$lte"] = seats_filter["max"]
                    else:
                        query["seats"] = {"$lte": seats_filter["max"]}
            elif isinstance(seats_filter, int):
                query["seats"] = {"$gte": seats_filter}
        
        # Filtro de potencia (horsepower)
        if "horsepower" in filters:
            hp_filter = filters["horsepower"]
            if isinstance(hp_filter, dict):
                if "min" in hp_filter:
                    query["horsepower"] = {"$gte": hp_filter["min"]}
                if "max" in hp_filter:
                    if "horsepower" in query:
                        query["horsepower"]["$lte"] = hp_filter["max"]
                    else:
                        query["horsepower"] = {"$lte": hp_filter["max"]}
            elif isinstance(hp_filter, int):
                query["horsepower"] = {"$gte": hp_filter}
        
        # Filtro de tamaño (categoría)
        if "size_category" in filters:
            size_cat = filters["size_category"].lower()
            if size_cat in self.size_mapping:
                size_rules = self.size_mapping[size_cat]
                # Aplicar reglas de tamaño
                for field, condition in size_rules.items():
                    if field in query:
                        # Combinar condiciones
                        if isinstance(query[field], dict) and isinstance(condition, dict):
                            query[field].update(condition)
                        else:
                            query[field] = condition
                    else:
                        query[field] = condition
        
        # Filtro de tipo de vehículo (solo si el campo existe en la DB)
        if "type" in filters:
            vehicle_type = filters["type"]
            if isinstance(vehicle_type, str) and vehicle_type.strip():
                # Normalizar tipos comunes
                type_mapping = {
                    "suv": "SUV",
                    "sedan": "Sedan",
                    "hatchback": "Hatchback",
                    "pickup": "Pickup",
                    "van": "Van"
                }
                normalized_type = type_mapping.get(vehicle_type.lower(), vehicle_type)
                # Solo agregar el filtro si hay valor válido
                if normalized_type:
                    query["type"] = normalized_type
            elif isinstance(vehicle_type, list) and len(vehicle_type) > 0:
                query["type"] = {"$in": vehicle_type}
        
        # Filtro de marca
        if "brand" in filters:
            brands = filters["brand"]
            if isinstance(brands, str):
                query["brand"] = brands
            elif isinstance(brands, list) and len(brands) > 0:
                query["brand"] = {"$in": brands}
        
        # Filtro de tipo de combustible
        if "fuel_type" in filters:
            fuel_type = filters["fuel_type"]
            if isinstance(fuel_type, str):
                query["fuel_type"] = fuel_type
            elif isinstance(fuel_type, list):
                query["fuel_type"] = {"$in": fuel_type}
        
        # Filtro de transmisión
        if "transmission" in filters:
            transmission = filters["transmission"]
            if isinstance(transmission, str):
                query["transmission"] = transmission
            elif isinstance(transmission, list):
                query["transmission"] = {"$in": transmission}
        
        # Filtro de año
        if "year" in filters:
            year_filter = filters["year"]
            if isinstance(year_filter, dict):
                if "min" in year_filter:
                    query["year"] = {"$gte": year_filter["min"]}
                if "max" in year_filter:
                    if "year" in query:
                        query["year"]["$lte"] = year_filter["max"]
                    else:
                        query["year"] = {"$lte": year_filter["max"]}
            elif isinstance(year_filter, int):
                query["year"] = {"$gte": year_filter}
        
        return query
    
    async def search_cars_with_filters(
        self, 
        filters: Dict[str, Any], 
        limit: int = 5,
        relax_filters: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Busca autos usando filtros estructurados.
        
        Args:
            filters: Filtros estructurados
            limit: Número máximo de resultados
            relax_filters: Si True, relaja filtros si no hay resultados
            
        Returns:
            List[Dict]: Lista de autos encontrados
        """
        try:
            # Construir query inicial
            query = self._build_mongo_query(filters)
            
            logger.info(f"Buscando autos con query: {query}")
            
            # Buscar autos
            cursor = self.cars_collection.find(query).limit(limit * 2)  # Buscar más para ordenar
            cars = list(cursor)
            
            # Si no hay resultados y relax_filters está activado, relajar filtros
            if len(cars) == 0 and relax_filters:
                logger.info("No se encontraron resultados, relajando filtros...")
                relaxed_filters = self._relax_filters(filters)
                query = self._build_mongo_query(relaxed_filters)
                cursor = self.cars_collection.find(query).limit(limit * 2)
                cars = list(cursor)
            
            # Convertir a formato de respuesta
            results = []
            for car in cars[:limit]:
                try:
                    car_dict = car_schema(car)
                    car_dict["id"] = str(car["_id"])
                    results.append(car_dict)
                except Exception as e:
                    logger.error(f"Error procesando auto {car.get('_id')}: {e}")
                    continue
            
            logger.info(f"Encontrados {len(results)} autos")
            return results
            
        except Exception as e:
            logger.error(f"Error buscando autos: {e}")
            return []
    
    def _relax_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Relaja los filtros para obtener más resultados.
        Elimina filtros menos críticos y amplía rangos.
        """
        relaxed = filters.copy()
        
        # Relajar precio (aumentar máximo en 20%)
        if "price" in relaxed and isinstance(relaxed["price"], dict):
            if "max" in relaxed["price"]:
                relaxed["price"]["max"] = int(relaxed["price"]["max"] * 1.2)
        
        # Relajar asientos (reducir mínimo en 1)
        if "seats" in relaxed and isinstance(relaxed["seats"], dict):
            if "min" in relaxed["seats"] and relaxed["seats"]["min"] > 2:
                relaxed["seats"]["min"] = relaxed["seats"]["min"] - 1
        
        # Relajar potencia (reducir mínimo en 20%)
        if "horsepower" in relaxed and isinstance(relaxed["horsepower"], dict):
            if "min" in relaxed["horsepower"]:
                relaxed["horsepower"]["min"] = int(relaxed["horsepower"]["min"] * 0.8)
        
        # Relajar año (reducir mínimo en 2 años)
        if "year" in relaxed and isinstance(relaxed["year"], dict):
            if "min" in relaxed["year"]:
                relaxed["year"]["min"] = relaxed["year"]["min"] - 2
        
        # Eliminar filtros menos críticos o que pueden no existir en la DB
        # type y size_category pueden no existir en los documentos de la DB
        filters_to_remove = ["brand", "color", "transmission", "type", "size_category", "fuel_type"]
        for key in filters_to_remove:
            if key in relaxed:
                del relaxed[key]
        
        return relaxed
    
    async def get_car_by_id(self, car_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un auto por su ID.
        
        Args:
            car_id: ID del auto
            
        Returns:
            dict: Auto encontrado o None
        """
        try:
            car = self.cars_collection.find_one({"_id": ObjectId(car_id)})
            if car:
                car_dict = car_schema(car)
                car_dict["id"] = str(car["_id"])
                return car_dict
            return None
        except Exception as e:
            logger.error(f"Error obteniendo auto {car_id}: {e}")
            return None


# Instancia global del servicio
_car_search_service: Optional[CarSearchService] = None


def get_car_search_service() -> CarSearchService:
    """Obtiene la instancia global del servicio de búsqueda (singleton)"""
    global _car_search_service
    if _car_search_service is None:
        _car_search_service = CarSearchService()
    return _car_search_service

