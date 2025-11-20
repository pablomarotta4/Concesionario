import logging
from typing import Dict, Any, List, Optional
from chatbot.llm_service import get_ollama_service
from chatbot.filter_extractor import get_filter_extractor
from services.car_search_service import get_car_search_service

logger = logging.getLogger(__name__)


class ConversationalAgent:
    """
    Agente conversacional que gestiona conversaciones multi-turn con contexto,
    extrae preferencias, busca autos y genera respuestas naturales.
    """
    
    def __init__(self):
        self.llm_service = get_ollama_service()
        self.filter_extractor = get_filter_extractor()
        self.car_search_service = get_car_search_service()
        
        # Almacenar sesiones de conversación (en producción usar Redis o DB)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        logger.info("ConversationalAgent inicializado")
    
    def _get_session(self, session_id: str) -> Dict[str, Any]:
        """Obtiene o crea una sesión de conversación"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "conversation_history": [],
                "extracted_filters": {},
                "last_cars": []
            }
        return self.sessions[session_id]
    
    async def handle_message(
        self, 
        user_message: str, 
        session_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario y retorna respuesta con recomendaciones.
        
        Args:
            user_message: Mensaje del usuario
            session_id: ID de sesión para mantener contexto
            
        Returns:
            dict: {
                "response": str,  # Respuesta conversacional
                "cars": List[Dict],  # Autos recomendados
                "filters_extracted": Dict,  # Filtros aplicados
                "needs_clarification": bool,  # Si necesita más info
                "clarification_question": Optional[str]  # Pregunta si necesita clarificación
            }
        """
        try:
            session = self._get_session(session_id)
            conversation_history = session["conversation_history"]
            
            # Agregar mensaje del usuario al historial
            conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Extraer filtros del mensaje
            filters = await self.filter_extractor.extract_filters_from_message(
                user_message,
                conversation_history
            )
            
            # Combinar con filtros previos (acumular información)
            previous_filters = session.get("extracted_filters", {})
            combined_filters = self._merge_filters(previous_filters, filters)
            session["extracted_filters"] = combined_filters
            
            # Validar filtros
            is_valid, error_msg = self.filter_extractor.validate_filters(combined_filters)
            if not is_valid:
                logger.warning(f"Filtros inválidos: {error_msg}")
                # Limpiar filtros inválidos y pedir clarificación
                session["extracted_filters"] = {}
                clarification = await self.llm_service.generate_clarification_question(
                    ["preferencias válidas"],
                    {"error": error_msg}
                )
                return {
                    "response": clarification,
                    "cars": [],
                    "filters_extracted": {},
                    "needs_clarification": True,
                    "clarification_question": clarification
                }
            
            # Verificar si necesitamos más información
            missing_info = self.filter_extractor.identify_missing_info(combined_filters)
            
            # Si no hay filtros o faltan datos críticos, SIEMPRE pedir clarificación (una pregunta a la vez)
            critical_missing = ["presupuesto", "tamaño o número de asientos"]
            has_critical_missing = any(item in missing_info for item in critical_missing)
            has_no_filters = len(combined_filters) == 0
            
            # Priorizar hacer preguntas antes de buscar autos si falta información crítica o no hay filtros
            if (has_critical_missing or has_no_filters) and missing_info:
                # Tomar solo la primera pregunta faltante
                clarification = await self.llm_service.generate_clarification_question(
                    [missing_info[0]],  # Solo UNA pregunta
                    {"conversation": conversation_history[-2:]}  # Solo últimos 2 mensajes para contexto
                )
                conversation_history.append({
                    "role": "assistant",
                    "content": clarification
                })
                return {
                    "response": clarification,
                    "cars": [],
                    "filters_extracted": combined_filters,
                    "needs_clarification": True,
                    "clarification_question": clarification
                }
            
            # Buscar autos con los filtros
            cars = await self.car_search_service.search_cars_with_filters(
                combined_filters,
                limit=5
            )
            
            session["last_cars"] = cars
            
            # Generar respuesta conversacional
            if cars:
                response = await self.llm_service.generate_conversational_response(
                    cars,
                    combined_filters,
                    conversation_history
                )
            else:
                # No se encontraron autos
                response = await self._handle_no_results(combined_filters, conversation_history)
            
            # Agregar respuesta al historial
            conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Limitar tamaño del historial (mantener últimos 10 mensajes)
            if len(conversation_history) > 10:
                session["conversation_history"] = conversation_history[-10:]
            
            return {
                "response": response,
                "cars": cars,
                "filters_extracted": combined_filters,
                "needs_clarification": False,
                "clarification_question": None
            }
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}", exc_info=True)
            return {
                "response": "Lo siento, hubo un error procesando tu mensaje. ¿Podrías intentar de nuevo?",
                "cars": [],
                "filters_extracted": {},
                "needs_clarification": False,
                "clarification_question": None
            }
    
    def _merge_filters(
        self, 
        previous: Dict[str, Any], 
        new: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Combina filtros previos con nuevos, priorizando los más específicos.
        """
        merged = previous.copy()
        
        for key, value in new.items():
            if key not in merged:
                merged[key] = value
            else:
                # Combinar valores según el tipo
                if isinstance(value, dict) and isinstance(merged[key], dict):
                    # Para rangos, tomar el más restrictivo
                    if "min" in value and "min" in merged[key]:
                        merged[key]["min"] = max(value["min"], merged[key]["min"])
                    elif "min" in value:
                        merged[key]["min"] = value["min"]
                    
                    if "max" in value and "max" in merged[key]:
                        merged[key]["max"] = min(value["max"], merged[key]["max"])
                    elif "max" in value:
                        merged[key]["max"] = value["max"]
                elif isinstance(value, list) and isinstance(merged[key], list):
                    # Para listas, unir y eliminar duplicados
                    merged[key] = list(set(merged[key] + value))
                else:
                    # Priorizar el nuevo valor
                    merged[key] = value
        
        return merged
    
    async def _handle_no_results(
        self, 
        filters: Dict[str, Any],
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """Maneja el caso cuando no se encuentran autos"""
        try:
            system_prompt = """Eres un asistente amigable de un concesionario.
            Cuando no encuentras autos, sugiere otras opciones de forma natural.
            CRÍTICO: 
            - NO uses palabras técnicas como "filtros", "criterios", "parámetros", "ajustar", "rango".
            - Habla como un vendedor humano: "¿Qué tal si buscamos algo más económico?" o "¿Te gustaría ver modelos de otro año?".
            - Sé breve (máximo 40 palabras)."""
            
            user_prompt = f"""No encontré autos con estas características: {filters}
            Genera una sugerencia amigable para ver otras opciones.
            RECUERDA: No menciones "filtros" ni "ajustar criterios". Pregunta sobre preferencias."""
            
            response = await self.llm_service.generate_response(
                [{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                max_tokens=100
            )
            
            # Limitar a 300 caracteres
            if len(response) > 300:
                sentences = response.split('.')
                response = sentences[0].strip() + '.' if sentences else response[:300]
            
            return response
        except:
            return "No encontré autos que coincidan. ¿Te gustaría ajustar tus criterios?"
    
    def reset_session(self, session_id: str = "default"):
        """Reinicia una sesión de conversación"""
        if session_id in self.sessions:
            self.sessions[session_id] = {
                "conversation_history": [],
                "extracted_filters": {},
                "last_cars": []
            }
        logger.info(f"Sesión {session_id} reiniciada")
    
    def get_session_info(self, session_id: str = "default") -> Dict[str, Any]:
        """Obtiene información de una sesión"""
        session = self._get_session(session_id)
        return {
            "session_id": session_id,
            "message_count": len(session["conversation_history"]),
            "filters_count": len(session.get("extracted_filters", {})),
            "last_cars_count": len(session.get("last_cars", []))
        }
