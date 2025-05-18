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
from memory.shared_memory import shared_history
from langchain_core.runnables import RunnableWithMessageHistory

smalltalk_llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0.45,
    streaming=False,
    api_key=API_KEY,
)

# 2) Memória simples para manter o contexto da conversa
# smalltalk_memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     return_messages=True,
# )

# 3) Prompt “chat” enxuto para smalltalk
smalltalk_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Histórico da conversa:\n{chat_history}\n\n"
        "Usuário: {input}\n"
    ),
])

# 4) Cadeia de conversação que usa memória
smalltalk_chain = RunnableWithMessageHistory(
    smalltalk_prompt | smalltalk_llm,
    shared_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
