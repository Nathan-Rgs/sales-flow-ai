from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from constants import API_KEY, LLM_MODEL, PRICE_SYSTEM_PROMPT
from vectorstore import retriever as price_retriever
from memory.shared_memory import shared_history
from langchain_core.runnables import RunnableWithMessageHistory

price_llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0.0,
    streaming=False,
    api_key=API_KEY,
)

# --- 2) Memória resumida para manter o histórico enxuto ---
# price_memory = ConversationBufferWindowMemory(
#     memory_key="chat_history",
#     input_key="question",
#     output_key="answer",
#     return_messages=True,
#     k=1
# )

# --- 3) Prompt para extração de preço ---
price_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        PRICE_SYSTEM_PROMPT
    ),
    HumanMessagePromptTemplate.from_template(
        "Responda **EXATAMENTE** o valor em reais, e complemente com as informações necessárias. \n"
        "Histórico da conversa:\n{chat_history}\n\n"
        "Catálogo de produtos:\n{context}\n\n"
        "Pergunta: Qual é o preço em reais do produto “{question}”?\n"
    ),
])

# --- 4) Cadeia de preço (modo stuff) ---
price_chain_base = ConversationalRetrievalChain.from_llm(
    llm=price_llm,
    retriever=price_retriever,
    return_source_documents=True,
    chain_type="stuff",
    combine_docs_chain_kwargs={"prompt": price_prompt},
)
price_chain = RunnableWithMessageHistory(
    price_chain_base,
    shared_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)
