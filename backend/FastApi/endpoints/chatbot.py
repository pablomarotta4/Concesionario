from fastapi import APIRouter, Request
from chatbot.agent import ConversationalAgent

router = APIRouter()

# Instancia global del agente (puedes mejorar esto con sesiones por usuario)
agent = ConversationalAgent()

@router.post("/chatbot/message")
async def chatbot_message(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    response = agent.handle_message(user_message)
    return {"response": response}
