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
from constants import API_KEY, LLM_MODEL, OLLAMA_URL, GENERIC_SYSTEM_PROMPT
from vectorstore import retriever

# --- 1) Instância do LLM ---
# llm = ChatOllama(
#     model=LLM_MODEL,
#     base_url=OLLAMA_URL,
#     temperature=0.3,
#     streaming=False,
# )

llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0.3,
    streaming=False,
    api_key=API_KEY,
)

# --- 2) Memória combinada ---
buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    output_key="answer",
    return_messages=True
)
summary_memory = ConversationSummaryMemory(
    llm=llm,
    input_key="question",
    output_key="answer",
    summary_key="history",
    max_token_limit=800,
)
combined_memory = CombinedMemory(memories=[buffer_memory, summary_memory], memory_key="combined_memory")

# --- 3) Definição dos prompts ---
question_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Resumo do que falamos:\n\n{history}\n\n"
        "contextos recuperados:\n\n{context}\n\n"
        "Pergunta:\n\n{question}"
    ),
])
refine_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Histórico completo:\n\n{chat_history}\n\n"
        "Resumo do que falamos:\n\n{history}\n\n"
        "Pergunta original:\n\n{question}\n\n"
        "Resposta-base até agora:\n\n{existing_answer}\n\n"
        "Novos contextos:\n\n{context}\n\n"
        "Por favor, refine a resposta mantendo-se fiel às fontes e ao histórico."
    ),
])

# --- 4) Construção da ConversationalRetrievalChain ---
info_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=combined_memory,
    return_source_documents=True,
    chain_type="refine",
    combine_docs_chain_kwargs={
        "question_prompt": question_prompt,
        "refine_prompt": refine_prompt,
        "document_variable_name": "context",
    },
)
