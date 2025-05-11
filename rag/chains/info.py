# chains/info.py

from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import (
    CombinedMemory,
    ConversationBufferMemory,
    ConversationSummaryMemory,
)
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
from constants import API_KEY, LLM_MODEL, GENERIC_SYSTEM_PROMPT
from vectorstore import retriever
from memory.shared_memory import shared_history
from langchain_core.runnables import RunnableWithMessageHistory

llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0.3,
    streaming=False,
    api_key=API_KEY,
)

# --- 2) Memória combinada ---
# buffer_memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     input_key="question",
#     output_key="answer",
#     return_messages=True
# )

# --- 3) Definição dos prompts ---
question_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Histórico da conversa:\n\n{chat_history}\n\n"
        "Contextos recuperados:\n\n{context}\n\n"
        "Pergunta:\n\n{question}"
    ),
])
refine_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Histórico da conversa:\n\n{chat_history}\n\n"
        "Pergunta original:\n\n{question}\n\n"
        "Resposta-base até agora:\n\n{existing_answer}\n\n"
        "Novos contextos:\n\n{context}\n\n"
        "Por favor, refine a resposta mantendo-se fiel às fontes e ao histórico."
    ),
])

# --- 4) Construção da ConversationalRetrievalChain ---
info_chain_base = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type="refine",
    combine_docs_chain_kwargs={
        "question_prompt": question_prompt,
        "refine_prompt": refine_prompt,
        "document_variable_name": "context",
    },
)
info_chain = RunnableWithMessageHistory(
    info_chain_base,
    shared_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)
