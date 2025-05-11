# project_root/chains/router.py

from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from constants import API_KEY, LLM_MODEL, OLLAMA_URL

# 1) LLM configurado com temperatura zero para classificação determinística
# router_llm = ChatOllama(
#     model=LLM_MODEL,
#     base_url=OLLAMA_URL,
#     temperature=0.0,
#     streaming=False,
# )

router_llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0.0,
    streaming=False,
    api_key=API_KEY,
)

# 2) Prompt em formato “chat” para roteamento de intenções
router_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "Você é um roteador de intenções. Classifique a mensagem do usuário em exatamente uma destas categorias: "
        "- price (quando o usuário quer saber preço)  "
        "- info (quando o usuário pede informação sobre o produtos, processos ou sobre a)  "
        "- smalltalk (quando for conversa casual sem dúvidas técnicas ou necessidade de recuperação de contexto)\n\n"
        "Retorne somente a etiqueta em caixa baixa, sem comentários extra."
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
])

# 3) LLMChain que combina o prompt + o LLM
router_chain = router_prompt | router_llm
