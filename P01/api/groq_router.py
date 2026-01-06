from dotenv import load_dotenv
from fastapi import APIRouter, Request
import os
from langchain_groq import ChatGroq

# Carrega a chave de ambiente
load_dotenv()

router = APIRouter()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY não encontrada no .env")



def enviar_mensagem(usuario_input):

    # Inicializa o modelo ChatGroq
    chat_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=300,
        api_key=api_key
    )

    # Inicializa o histórico com uma mensagem de sistema (opcional, mas recomendado)
    conversation_history = [
        {"role": "system", "content": "Você é um assistente educado, paciente e motivador."}
    ]

    # Adiciona a mensagem do usuário ao histórico
    conversation_history.append({"role": "user", "content": usuario_input})

    resposta_do_gpt = chat_llm.invoke(conversation_history).content

    # Adiciona a resposta do GPT ao histórico
    conversation_history.append({"role": "assistant", "content": resposta_do_gpt})

    return resposta_do_gpt

@router.get("/chat")
def chat(msg: str):
    resposta = enviar_mensagem(msg)
    return {
        "resposta": resposta
    }

""" # Exemplo de uso:
while True:
    entrada = input("Você: ")
    if entrada.lower() in ["sair", "exit"]:
        break
    resposta = enviar_mensagem(entrada)
    print("Chatbot:", resposta) """