from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Carrega a chave de ambiente
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY não encontrada no .env")

chatgpt = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

prompt = "Gere um texto de 2 parágrafos sobre dicas de saúde"

template = ChatPromptTemplate.from_messages([
    ("system", "Você é um redator profissional"),
    ("human", "{prompt}")
])

chain_chatgpt = template | chatgpt

res = chain_chatgpt.invoke({"prompt": prompt})
print(res.content)