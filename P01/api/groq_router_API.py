from fastapi import APIRouter
from service.groq_router_service import GroqRouterClass
from service.groq_router_chain_service import GroqRouterChainClass
router = APIRouter()

groq_router = GroqRouterClass()
groq_router_chain = GroqRouterChainClass()

@router.get("/chat_chain")
async def chat_chain(msg: str) -> str:
    resposta = groq_router_chain.enviar_mensagem(msg)
    return resposta

@router.get("/chat")
async def chat(msg: str) -> str:
    resposta = groq_router.enviar_mensagem(msg)
    return resposta

