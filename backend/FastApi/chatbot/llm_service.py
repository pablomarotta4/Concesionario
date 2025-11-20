import os
import httpx
import json
import logging
import re
from typing import List, Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class OllamaService:
    """
    Servicio para interactuar con Ollama API local.
    Maneja la generación de respuestas conversacionales y extracción de filtros.
    """
    
    def __init__(self, base_url: str = None, model: str = None):
        """
        Inicializa el servicio de Ollama.
        
        Args:
            base_url: URL base de Ollama (default: desde env o http://localhost:11434)
            model: Nombre del modelo a usar (default: desde env o llama3.2:3b)
        """
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        self.client = httpx.AsyncClient(timeout=60.0)
        
        logger.info(f"OllamaService inicializado: {self.base_url}, modelo: {self.model}")
    
    async def _check_connection(self) -> bool:
        """Verifica que Ollama esté disponible"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error conectando a Ollama: {e}")
            return False
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> str:
        """
        Genera una respuesta conversacional usando el LLM.
        
        Args:
            messages: Lista de mensajes en formato [{"role": "user", "content": "..."}]
            system_prompt: Prompt del sistema (opcional)
            temperature: Temperatura para la generación (0.0-1.0)
            max_tokens: Número máximo de tokens a generar (opcional)
            
        Returns:
            str: Respuesta generada por el modelo
        """
        try:
            # Construir el prompt completo
            prompt_parts = []
            
            if system_prompt:
                prompt_parts.append(f"System: {system_prompt}\n\n")
            
            # Convertir mensajes a formato de prompt
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    prompt_parts.append(f"System: {content}\n\n")
                elif role == "user":
                    prompt_parts.append(f"User: {content}\n\n")
                elif role == "assistant":
                    prompt_parts.append(f"Assistant: {content}\n\n")
            
            prompt_parts.append("Assistant: ")
            full_prompt = "".join(prompt_parts)
            
            # Llamar a la API de Ollama
            options = {
                "temperature": temperature
            }
            if max_tokens:
                options["num_predict"] = max_tokens  # Ollama usa num_predict en lugar de max_tokens
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": options
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except httpx.HTTPError as e:
            logger.error(f"Error HTTP al generar respuesta: {e}")
            raise Exception(f"Error conectando con Ollama: {str(e)}")
        except Exception as e:
            logger.error(f"Error inesperado al generar respuesta: {e}")
            raise
    
    async def extract_filters(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Extrae filtros estructurados del mensaje del usuario usando LLM.
        
        Args:
            user_message: Mensaje del usuario
            conversation_history: Historial de conversación (opcional)
            
        Returns:
            dict: Filtros extraídos en formato JSON estructurado
        """
        try:
            # Construir contexto de la conversación
            context = ""
            if conversation_history:
                context = "\n".join([
                    f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                    for msg in conversation_history[-5:]  # Últimos 5 mensajes
                ])
            
            system_prompt = """Eres un asistente experto en extraer preferencias de usuarios sobre autos.
Analiza el mensaje del usuario y extrae filtros estructurados en formato JSON.

Debes retornar SOLO un JSON válido con los siguientes campos posibles:
{
  "price": {"min": 0, "max": 50000},
  "seats": {"min": 5},
  "horsepower": {"min": 150},
  "size_category": "large|medium|small",
  "type": "SUV|Sedan|Hatchback|Pickup|Van",
  "brand": ["Toyota", "BMW"],
  "fuel_type": "Gasolina|Diesel|Híbrido|Eléctrico",
  "transmission": "Manual|Automatic",
  "year": {"min": 2020}
}

Si el usuario no menciona algo, NO lo incluyas en el JSON.
Retorna SOLO el JSON, sin texto adicional."""

            # Construir el contexto de forma separada (evita error de backslash en f-string)
            context_text = ""
            if context:
                context_text = f"Contexto de la conversación:\n{context}\n"

            user_prompt = f"""Mensaje del usuario: {user_message}

{context_text}Extrae los filtros en formato JSON:"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = await self.generate_response(messages, temperature=0.3)
            
            # Intentar parsear el JSON de la respuesta
            # El LLM puede devolver texto antes/después del JSON
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                filters = json.loads(json_str)
                return filters
            else:
                logger.warning(f"No se pudo extraer JSON de la respuesta: {response}")
                return {}
                
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON de filtros: {e}, respuesta: {response}")
            return {}
        except Exception as e:
            logger.error(f"Error extrayendo filtros: {e}")
            return {}
    
    async def generate_clarification_question(
        self, 
        missing_info: List[str], 
        context: Dict[str, Any] = None
    ) -> str:
        """
        Genera UNA pregunta de clarificación cuando faltan datos importantes.
        Siempre pregunta solo UNA cosa a la vez.
        
        Args:
            missing_info: Lista de información faltante (solo usará la primera)
            context: Contexto adicional de la conversación
            
        Returns:
            str: Pregunta de clarificación (una sola pregunta, máximo 20 palabras)
        """
        try:
            system_prompt = """Eres un asistente amigable de un concesionario de autos.
            Genera UNA pregunta breve y natural para conocer mejor lo que busca el cliente.
            CRÍTICO - REGLAS DE ESTILO:
            - NUNCA uses palabras como "filtros", "parámetros", "criterios", "configuración", "rango".
            - Habla de "preferencias", "gustos", "necesidades", "lo que buscas".
            - Haz SOLO UNA pregunta a la vez.
            - No te extiendas mucho, preguntas concisas.
            - Sé directo y amigable, como una conversación casual."""

            # Tomar solo la primera información faltante
            first_missing = missing_info[0] if missing_info else "tus preferencias"
            
            # Traducir términos técnicos a lenguaje natural
            missing_map = {
                "presupuesto": "cuánto te gustaría invertir", "cual es tu presupuesto"
                "tamaño o número de asientos": "qué tamaño de auto necesitas",
                "price": "tu presupuesto",
                "seats": "cuántas personas viajarán",
                "horsepower": "la potencia del motor",
                "brand": "si tienes alguna marca favorita"
            }
            natural_missing = missing_map.get(first_missing, first_missing)
            
            context_str = ""
            if context and "conversation" in context:
                # Extraer último mensaje del usuario para contexto
                conv = context.get("conversation", [])
                if conv:
                    last_user_msg = [m.get("content", "") for m in conv if m.get("role") == "user"]
                    if last_user_msg:
                        context_str = f"\nEl cliente dijo: \"{last_user_msg[-1]}\""
            
            user_prompt = f"""Necesito preguntar amablemente sobre: {natural_missing}
            {context_str}
            
            Genera UNA pregunta natural (sin mencionar "filtros" ni palabras técnicas):"""

            messages = [{"role": "user", "content": user_prompt}]
            
            response = await self.generate_response(
                messages, 
                system_prompt=system_prompt, 
                temperature=0.7,
                max_tokens=50  # Limitar tokens para respuestas cortas
            )
            
            # Limitar longitud manualmente (máximo 150 caracteres)
            response = response.strip()
            if len(response) > 150:
                # Tomar solo la primera oración
                sentences = response.split('.')
                response = sentences[0].strip() + '.' if sentences else response[:150]
            
            return response
            
        except Exception as e:
            logger.error(f"Error generando pregunta de clarificación: {e}")
            # Fallback a pregunta genérica
            return f"¿Podrías contarme sobre {missing_info[0] if missing_info else 'tus preferencias'}?"
    
    async def generate_conversational_response(
        self,
        cars: List[Dict[str, Any]],
        filters: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Genera una respuesta conversacional breve con las recomendaciones de autos.
        
        Args:
            cars: Lista de autos recomendados
            filters: Filtros aplicados
            conversation_history: Historial de conversación
            
        Returns:
            str: Respuesta conversacional breve (máximo 150 palabras)
        """
        try:
            system_prompt = """Eres un asistente experto de un concesionario de autos.
Genera respuestas BREVES, naturales y amigables en español.
CRÍTICO - REGLAS ABSOLUTAS:
- SOLO menciona los autos que se te proporcionan en la lista. NUNCA inventes, sugieras o menciones otros autos.
- NO menciones Toyota Corolla, Honda Civic u otros autos a menos que estén explícitamente en la lista proporcionada.
- Máximo 150 palabras
- Presenta los autos de forma concisa
- Menciona solo las características más importantes (precio, marca, modelo, año)
- No hagas listas largas ni descripciones extensas
- Sé directo y profesional"""

            # Preparar información de autos (TODOS los autos, no solo 3)
            cars_info = []
            for i, car in enumerate(cars, 1):  # Mostrar TODOS los autos
                car_str = f"{car.get('brand', '')} {car.get('model', '')} {car.get('year', '')}"
                car_str += f" - ${car.get('price', 0):,.0f}"
                if car.get('seats'):
                    car_str += f" - {car.get('seats')} asientos"
                cars_info.append(car_str)
            
            cars_text = "\n".join(cars_info) if cars_info else "No encontré autos que coincidan exactamente."
            
            user_prompt = f"""Lista EXACTA de autos disponibles para el cliente (SOLO menciona estos, NUNCA otros):

{cars_text}

Genera una respuesta BREVE (máximo 150 palabras) presentando ÚNICAMENTE estos autos de la lista.
IMPORTANTE: NO inventes, sugieras o menciones ningún otro auto que no esté en la lista de arriba.
Menciona solo lo esencial: marca, modelo, año y precio.
Sé directo y amigable."""

            messages = [{"role": "user", "content": user_prompt}]
            
            if conversation_history:
                # Agregar contexto de la conversación (solo último mensaje)
                last_msg = conversation_history[-1] if conversation_history else None
                if last_msg and last_msg.get("role") == "user":
                    messages.insert(0, last_msg)
            
            response = await self.generate_response(
                messages, 
                system_prompt=system_prompt, 
                temperature=0.3,  # Reducir temperatura para ser más determinista y seguir instrucciones
                max_tokens=500  # Limitar tokens para respuestas más cortas
            )
            
            # Filtrar menciones de autos que no están en la lista proporcionada
            # Extraer marcas y modelos de los autos proporcionados
            provided_cars = set()
            for car in cars[:3]:
                brand = car.get('brand', '').lower()
                model = car.get('model', '').lower()
                if brand and model:
                    provided_cars.add(f"{brand} {model}")
                    provided_cars.add(brand)
                    provided_cars.add(model)
            
            # Verificar si la respuesta menciona autos no proporcionados
            response_lower = response.lower()
            # Lista de autos comunes que el LLM podría mencionar incorrectamente
            common_cars_to_filter = ['toyota corolla', 'honda civic', 'corolla', 'civic']
            for car_name in common_cars_to_filter:
                if car_name not in provided_cars and car_name in response_lower:
                    # Reemplazar menciones no deseadas
                    # Patrón para encontrar menciones del auto no deseado
                    pattern = re.compile(r'\b' + re.escape(car_name) + r'\b', re.IGNORECASE)
                    if pattern.search(response):
                        logger.warning(f"Filtrado mención no deseada de '{car_name}' en respuesta")
                        # Eliminar oraciones que mencionen estos autos
                        sentences = response.split('.')
                        filtered_sentences = []
                        for sentence in sentences:
                            sentence_lower = sentence.lower()
                            should_include = True
                            for unwanted_car in common_cars_to_filter:
                                if unwanted_car not in provided_cars and unwanted_car in sentence_lower:
                                    should_include = False
                                    break
                            if should_include:
                                filtered_sentences.append(sentence)
                        response = '. '.join(filtered_sentences).strip()
                        if response and not response.endswith('.'):
                            response += '.'
                        break
            
            # Limitar longitud manualmente (máximo 800 caracteres ~ 150 palabras)
            response = response.strip()
            if len(response) > 800:
                # Tomar solo las primeras oraciones hasta llegar al límite
                sentences = response.split('.')
                result = []
                for sentence in sentences:
                    if len('. '.join(result + [sentence])) <= 800:
                        result.append(sentence)
                    else:
                        break
                response = '. '.join(result).strip()
                if response and not response.endswith('.'):
                    response += '.'
            
            return response
            
        except Exception as e:
            logger.error(f"Error generando respuesta conversacional: {e}")
            # Fallback a respuesta básica
            if cars:
                return f"Encontré {len(cars)} auto(s) que coinciden con tus preferencias. ¿Te gustaría ver más detalles?"
            else:
                return "No encontré autos que coincidan exactamente. ¿Quieres ajustar tus criterios de búsqueda?"
    
    async def close(self):
        """Cierra el cliente HTTP"""
        await self.client.aclose()
    
    def __del__(self):
        """Cleanup al destruir el objeto"""
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.client.aclose())
        except:
            pass


# Instancia global del servicio
_ollama_service: Optional[OllamaService] = None


def get_ollama_service() -> OllamaService:
    """Obtiene la instancia global del servicio Ollama (singleton)"""
    global _ollama_service
    if _ollama_service is None:
        _ollama_service = OllamaService()
    return _ollama_service

