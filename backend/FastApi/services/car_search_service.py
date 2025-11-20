from typing import List, Dict, Any, Optional
import random
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
            
            # Calculate relevance scores for intelligent ranking
            scored_results = []
            for car in cars:
                try:
                    car_dict = car_schema(car)
                    car_dict["id"] = str(car["_id"])
                    
                    # Calculate relevance score based on filters
                    score = self._calculate_relevance_score(car_dict, filters)
                    scored_results.append((car_dict, score))
                except Exception as e:
                    logger.error(f"Error procesando auto {car.get('_id')}: {e}")
                    continue
            
            # Sort by relevance score (highest first)
            scored_results.sort(key=lambda x: x[1], reverse=True)
            
            # Group into tiers for smart shuffling
            results = self._apply_tiered_variety(scored_results, limit)
            
            logger.info(f"Encontrados {len(results)} autos con scoring inteligente")
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
    
    def _calculate_relevance_score(self, car: Dict[str, Any], filters: Dict[str, Any]) -> float:
        """
        Calculate how well a car matches the given filters.
        Higher score = better match.
        
        Args:
            car: Car data
            filters: Applied filters
            
        Returns:
            float: Relevance score (0-100+)
        """
        score = 0.0
        
        # Exact type match is highly important (+15 points)
        if "type" in filters and car.get("type") == filters["type"]:
            score += 15
        
        # Brand match (+10 points)
        if "brand" in filters:
            if isinstance(filters["brand"], str) and car.get("brand") == filters["brand"]:
                score += 10
            elif isinstance(filters["brand"], list) and car.get("brand") in filters["brand"]:
                score += 10
        
        # Seats match (+12 points for exact match, +8 for being in range)
        if "seats" in filters:
            car_seats = car.get("seats", 0)
            filter_seats = filters["seats"]
            if isinstance(filter_seats, dict):
                min_seats = filter_seats.get("min", 0)
                max_seats = filter_seats.get("max", 100)
                if min_seats <= car_seats <= max_seats:
                    # Perfect range match
                    score += 12
                    # Bonus if close to minimum (what user wants)
                    if car_seats == min_seats or car_seats == min_seats + 1:
                        score += 3
            elif isinstance(filter_seats, int) and car_seats >= filter_seats:
                score += 12
        
        # Horsepower/Power match (+10 points)
        if "horsepower" in filters:
            car_hp = car.get("horsepower", 0)
            filter_hp = filters["horsepower"]
            if isinstance(filter_hp, dict):
                min_hp = filter_hp.get("min", 0)
                max_hp = filter_hp.get("max", 9999)
                if min_hp <= car_hp <= max_hp:
                    score += 10
                    # Bonus for exceeding minimum significantly
                    if car_hp >= min_hp + 50:
                        score += 5
            elif isinstance(filter_hp, int) and car_hp >= filter_hp:
                score += 10
        
        # Price match (+8 points for being in range, penalty for being too far)
        if "price" in filters:
            car_price = car.get("price", 0)
            filter_price = filters["price"]
            if isinstance(filter_price, dict):
                min_price = filter_price.get("min", 0)
                max_price = filter_price.get("max", 999999)
                if min_price <= car_price <= max_price:
                    score += 8
                    # Bonus for being near the max (user's budget)
                    price_range = max_price - min_price
                    if price_range > 0:
                        position = (car_price - min_price) / price_range
                        if 0.7 <= position <= 1.0:  # Near max budget
                            score += 3
                else:
                    # Penalty for being out of range
                    if car_price > max_price:
                        overage_pct = (car_price - max_price) / max_price
                        score -= min(10, overage_pct * 20)
            elif isinstance(filter_price, (int, float)) and car_price <= filter_price:
                score += 8
        
        # Year/Newness bonus (+1-5 points for newer cars)
        car_year = car.get("year", 2000)
        year_bonus = (car_year - 2018) * 0.5  # 0.5 points per year since 2018
        score += max(0, min(5, year_bonus))
        
        # Fuel type match (+6 points)
        if "fuel_type" in filters:
            car_fuel = car.get("fuel_type", "")
            filter_fuel = filters["fuel_type"]
            if isinstance(filter_fuel, str) and car_fuel == filter_fuel:
                score += 6
            elif isinstance(filter_fuel, list) and car_fuel in filter_fuel:
                score += 6
        
        # Transmission match (+4 points)
        if "transmission" in filters:
            car_trans = car.get("transmission", "")
            filter_trans = filters["transmission"]
            if isinstance(filter_trans, str) and filter_trans.lower() in car_trans.lower():
                score += 4
            elif isinstance(filter_trans, list):
                if any(ft.lower() in car_trans.lower() for ft in filter_trans):
                    score += 4
        
        # Size category match (+8 points)
        if "size_category" in filters:
            # This is already filtered by MongoDB, so if it's here, it matches
            score += 8
        
        return score
    
    def _apply_tiered_variety(self, scored_results: List[tuple], limit: int) -> List[Dict[str, Any]]:
        """
        Apply smart variety by shuffling within score tiers.
        This provides variety while maintaining relevance.
        
        Args:
            scored_results: List of (car_dict, score) tuples, sorted by score descending
            limit: Number of results to return
            
        Returns:
            List of car dictionaries
        """
        if not scored_results:
            return []
        
        # Define tier boundaries based on score distribution
        max_score = scored_results[0][1] if scored_results else 0
        
        # Tier 1: High relevance (within 10% of max score)
        # Tier 2: Medium relevance (within 30% of max score)  
        # Tier 3: Lower relevance (rest)
        tier1_threshold = max_score * 0.9
        tier2_threshold = max_score * 0.7
        
        tier1 = [(car, score) for car, score in scored_results if score >= tier1_threshold]
        tier2 = [(car, score) for car, score in scored_results if tier2_threshold <= score < tier1_threshold]
        tier3 = [(car, score) for car, score in scored_results if score < tier2_threshold]
        
        # Shuffle within each tier for variety
        random.shuffle(tier1)
        random.shuffle(tier2)
        random.shuffle(tier3)
        
        # Combine tiers and take top results
        all_tiers = tier1 + tier2 + tier3
        results = [car for car, score in all_tiers[:limit]]
        
        logger.info(f"Tier distribution: T1={len(tier1)}, T2={len(tier2)}, T3={len(tier3)}")
        
        return results
    
    def _relax_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Relaja los filtros para obtener más resultados.
        Elimina filtros menos críticos y amplía rangos.
        """
        relaxed = filters.copy()
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

