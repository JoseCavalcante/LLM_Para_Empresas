from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Carrega variáveis de ambiente
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY não encontrada no .env")

class GroqRouterChainClass:
    """
    Serviço profissional que utiliza LangChain Expression Language (LCEL)
    para encadear o prompt, o modelo e o parser de saída.
    """
    
    def __init__(self):
        # 1. Configuração do Modelo
        self.chat_llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=300,
            api_key=api_key
        )
        
        # 2. Definição do Prompt Profissional
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um especialista em marketing digital e inteligência artificial. "
                       "Sua missão é fornecer respostas precisas, criativas e profissionais. "
                       "Mantenha um tom consultivo e encorajador."),
            ("human", "{usuario_input}")
        ])
        
        # 3. Definição da Chain (LCEL)
        # O operador '|' encadeia os componentes de forma profissional:
        # Prompt -> Modelo -> Parser (Transforma o objeto de mensagem em string)
        self.chain = self.prompt_template | self.chat_llm | StrOutputParser()

    def enviar_mensagem(self, usuario_input: str) -> str:
        """
        Executa a chain de forma síncrona.
        """
        # Invocamos a chain passando o dicionário com as variáveis do template
        resposta = self.chain.invoke({"usuario_input": usuario_input})
        
        return resposta
