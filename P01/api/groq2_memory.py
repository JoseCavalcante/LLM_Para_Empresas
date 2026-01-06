from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# Carrega a chave de ambiente
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY não encontrada no .env")

# Inicializa o modelo ChatGroq
chat_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=300,
    api_key=api_key
)

# Histórico global
conversation_history = []

# Histórico de conversa inicial
conversation_history = [
    ("system", "Você é um assistente educado, paciente e motivador.")
]

def enviar_mensagem2222(usuario_input: str) -> str:
    
    # Adiciona a mensagem do usuário
    conversation_history.append(("human", usuario_input))

    template = ChatPromptTemplate.from_messages(conversation_history)

    chain = template | chat_llm | StrOutputParser()

    res = chain.invoke({})

    conversation_history.append(("ai", res))

    return res


def enviar_mensagem(usuario_input: str) -> str:
    
    # Adiciona a mensagem do usuário
    conversation_history.append({"role": "user", "content": usuario_input})

    # Chama o LLM apenas com mensagens válidas
    resposta_do_gpt = chat_llm.invoke(conversation_history).content

    # Adiciona a resposta limpa ao histórico
    conversation_history.append({"role": "assistant", "content": resposta_do_gpt})

    return resposta_do_gpt

# Loop de chat
if __name__ == "__main__":
    print("Chatbot iniciado! Digite 'sair' ou 'exit' para encerrar.")
    while True:
        entrada = input("Você: ")
        if entrada.lower() in ["sair", "exit"]:
            print("Encerrando chat...")
            break
        resposta = enviar_mensagem2222(entrada)
        print("Chatbot:", resposta)
