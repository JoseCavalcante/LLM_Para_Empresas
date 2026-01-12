from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Carrega variáveis de ambiente
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY não encontrada no .env")


class GroqRouterClass:

    def __init__(self):        

        self.chat_llm = ChatGroq(
                                model="llama-3.3-70b-versatile",
                                temperature=0.7,
                                max_tokens=300,
                                api_key=api_key
                                )

    def enviar_mensagem(self, usuario_input: str) -> str:

        messages = [
            SystemMessage(content="Você é um assistente educado, paciente e motivador."),
            HumanMessage(content=usuario_input)
        ]

        resposta_do_gpt = self.chat_llm.invoke(messages).content

        return resposta_do_gpt
