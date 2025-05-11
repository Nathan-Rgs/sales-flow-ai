from langchain_ollama import ChatOllama
from langchain.chains import ConversationChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from constants import API_KEY, LLM_MODEL, OLLAMA_URL, GENERIC_SYSTEM_PROMPT

# 1) LLM com temperatura um pouco mais alta para smalltalk
# smalltalk_llm = ChatOllama(
#     model=LLM_MODEL,
#     base_url=OLLAMA_URL,
#     temperature=0.7,    # respostas mais “soltas” e naturais
#     streaming=False,
# )

smalltalk_llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0.7,
    streaming=False,
    api_key=API_KEY,
)

# 2) Memória simples para manter o contexto da conversa
smalltalk_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

# 3) Prompt “chat” enxuto para smalltalk
smalltalk_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Histórico da conversa:\n{chat_history}\n\n"
        "Seja amigável e descontraído quando o usuário quiser apenas bater papo. Porém NÃO SAIA DO CONTEXTO (se sair informe que você não conhece/pode falar sobre tais assuntos), NEM SEJA ANTI PROFISSIONAL.\n"
        "Usuário: {input}\n"
    ),
])

# 4) Cadeia de conversação que usa memória
smalltalk_chain = ConversationChain(
    llm=smalltalk_llm,
    prompt=smalltalk_prompt,
    memory=smalltalk_memory,
)
