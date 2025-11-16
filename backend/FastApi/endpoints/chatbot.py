from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from chatbot.agent import ConversationalAgent
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])

# Instancia global del agente
agent = ConversationalAgent()


class ChatbotMessageRequest(BaseModel):
    """Request model para mensajes del chatbot"""
    message: str = Field(..., description="Mensaje del usuario")
    session_id: Optional[str] = Field(default="default", description="ID de sesión para mantener contexto")


class ChatbotMessageResponse(BaseModel):
    """Response model para respuestas del chatbot"""
    response: str = Field(..., description="Respuesta conversacional del chatbot")
    cars: List[Dict[str, Any]] = Field(default_factory=list, description="Autos recomendados")
    filters_extracted: Dict[str, Any] = Field(default_factory=dict, description="Filtros extraídos y aplicados")
    needs_clarification: bool = Field(default=False, description="Indica si el chatbot necesita más información")
    clarification_question: Optional[str] = Field(default=None, description="Pregunta de clarificación si aplica")
    session_id: str = Field(..., description="ID de sesión")


@router.post("/message", response_model=ChatbotMessageResponse)
async def chatbot_message(request: ChatbotMessageRequest):
    """
    Endpoint principal del chatbot.
    Recibe un mensaje del usuario y retorna una respuesta conversacional con recomendaciones.
    
    El chatbot mantiene contexto de la conversación usando session_id.
    """
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
        
        # Procesar mensaje con el agente
        result = await agent.handle_message(
            user_message=request.message,
            session_id=request.session_id
        )
        
        # Formatear autos con links de redirección (para implementación web futura)
        formatted_cars = []
        for car in result.get("cars", []):
            car_dict = dict(car)
            # Agregar link de redirección (formato para implementación web)
            car_id = car_dict.get("id", "")
            car_dict["link"] = f"/cars/{car_id}" if car_id else None
            formatted_cars.append(car_dict)
        
        return ChatbotMessageResponse(
            response=result.get("response", ""),
            cars=formatted_cars,
            filters_extracted=result.get("filters_extracted", {}),
            needs_clarification=result.get("needs_clarification", False),
            clarification_question=result.get("clarification_question"),
            session_id=request.session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint chatbot: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando mensaje: {str(e)}"
        )


@router.post("/reset")
async def reset_chatbot_session(session_id: str = "default"):
    """
    Reinicia una sesión de conversación del chatbot.
    Útil para comenzar una nueva búsqueda.
    """
    try:
        agent.reset_session(session_id)
        return {
            "message": f"Sesión {session_id} reiniciada correctamente",
            "session_id": session_id
        }
    except Exception as e:
        logger.error(f"Error reiniciando sesión: {e}")
        raise HTTPException(status_code=500, detail=f"Error reiniciando sesión: {str(e)}")


@router.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """
    Obtiene información sobre una sesión de conversación.
    """
    try:
        info = agent.get_session_info(session_id)
        return info
    except Exception as e:
        logger.error(f"Error obteniendo info de sesión: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo info de sesión: {str(e)}")


@router.get("/health")
async def chatbot_health():
    """
    Health check del chatbot.
    Verifica que los servicios estén disponibles.
    """
    try:
        # Verificar que el agente esté inicializado
        if agent is None:
            return {"status": "unhealthy", "reason": "Agent not initialized"}
        
        # Verificar servicios (opcional, puede ser pesado)
        # Por ahora solo retornamos healthy si el agente existe
        return {
            "status": "healthy",
            "service": "chatbot",
            "sessions_active": len(agent.sessions)
        }
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return {"status": "unhealthy", "reason": str(e)}
