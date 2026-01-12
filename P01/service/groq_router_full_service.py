from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# Carrega variáveis de ambiente
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY não encontrada no .env")

class GroqRouterFullService:
    """
    Serviço avançado de IA que utiliza LangChain LCEL e gestão automática de histórico.
    """
    
    def __init__(self):
        # 1. Configuração do Modelo
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=api_key
        )
        
        # 2. Template de Prompt com Histórico
        # O MessagesPlaceholder('history') é onde o LangChain injetará as mensagens anteriores
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é um consultor sênior de Marketing Digital. "
                       "Sua tarefa é ajudar o usuário com estratégias, copies e ideias criativas. "
                       "Responda sempre em Português do Brasil."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{usuario_input}")
        ])
        
        # 3. Definição da Chain Base
        self.chain = self.prompt | self.llm | StrOutputParser()
        
        # 4. Gerenciamento de Histórico em Memória
        # Dicionário para armazenar o histórico de cada sessão
        self.store = {}
        
        # 5. Chain com Histórico (RunnableWithMessageHistory)
        # Isso automatiza a busca e o salvamento das mensagens no histórico
        self.chain_with_history = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="usuario_input",
            history_messages_key="history"
        )

    def get_session_history(self, session_id: str):
        """Retorna ou cria o histórico para uma sessão específica."""
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def enviar_mensagem(self, usuario_input: str, session_id: str = "default") -> str:
        """
        Envia uma mensagem mantendo o contexto da sessão informada.
        """
        config = {"configurable": {"session_id": session_id}}
        
        # Invocamos a chain com o histórico automático
        resposta = self.chain_with_history.invoke(
            {"usuario_input": usuario_input},
            config=config
        )
        
        return resposta
