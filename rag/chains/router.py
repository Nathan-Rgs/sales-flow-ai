# project_root/chains/router.py

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from config import LLM_MODEL, OLLAMA_URL

# 1) Inicializa o LLM para classificação de intenções
router_llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.0,
    streaming=False
)

# 2) Prompt que mapeia mensagem → etiqueta de intenção
intent_prompt = PromptTemplate(
    input_variables=["input"],
    template="""
Classifique a mensagem em exatamente uma destas categorias:
- price
- info
- smalltalk
- chat

Retorne apenas a etiqueta (em caixa baixa).

Mensagem: {input}
""",
)

# 3) Cria o RunnableSequence substituindo LLMChain
#    Agora 'router' é a composição do prompt com o LLM
router = intent_prompt | router_llm
