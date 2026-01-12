from fastapi import APIRouter
from service.groq_router_full_service import GroqRouterFullService

router = APIRouter(prefix="/chat_full")

# Instanciamos o serviço (ele mantém o 'store' do histórico em memória)
groq_full_service = GroqRouterFullService()

@router.get("/")
async def chat_full(msg: str, session_id: str = "user_default"):
    """
    Endpoint avançado que mantém histórico de conversa por sessão.
    - msg: A mensagem do usuário.
    - session_id: Identificador único da conversa (ex: ID do usuário ou Aba do navegador).
    """
    resposta = groq_full_service.enviar_mensagem(msg, session_id)
    
    return {
        "session_id": session_id,
        "resposta": resposta
    }

@router.delete("/{session_id}")
async def reset_session(session_id: str):
    """Limpa o histórico de uma sessão específica."""
    if session_id in groq_full_service.store:
        del groq_full_service.store[session_id]
        return {"status": "success", "message": f"Histórico da sessão {session_id} foi resetado."}
    return {"status": "error", "message": "Sessão não encontrada."}
