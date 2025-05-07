from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import (
    CombinedMemory,
    ConversationBufferMemory,
    ConversationSummaryMemory,
)
from constants import (
    LLM_MODEL,
    OLLAMA_URL,
    EMBEDDINGS_MODEL,
    PERSIST_DIR,
    GENERIC_SYSTEM_PROMPT,
)

# --- 1) LLM e Retriever ---
llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.3,
    streaming=False,
)
emb = OllamaEmbeddings(
    model=EMBEDDINGS_MODEL,
    base_url=OLLAMA_URL,
)
vectordb = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=emb,
)
retriever = vectordb.as_retriever()

# --- 2) Memória combinada: buffer (chat_history) + resumo (history) ---
buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",   # histórico completo
    input_key="question",        # sua chave de entrada
    output_key="answer",         # nomeia a saída do chain
    return_messages=False,
)
summary_memory = ConversationSummaryMemory(
    llm=llm,
    input_key="question",        # mesma chave de entrada
    output_key="answer",         # mesma saída que o buffer
    summary_key="history",       # variá­vel que vai para o prompt
    max_token_limit=800,         # controla o tamanho do resumo
)
combined_memory = CombinedMemory(
    memories=[buffer_memory, summary_memory]
)

# --- 3) Prompts atualizados ---
question_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Resumo do que falamos:\n\n{history}\n\n"
        "Trechos recuperados:\n\n{context}\n\n"
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
        "Novos trechos:\n\n{context}\n\n"
        "Por favor, refine a resposta mantendo-se fiel às fontes e ao histórico."
    ),
])

# --- 4) Cadeia ConversationalRetrievalChain (modo refine) ---
info_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=combined_memory,            # usa a memória combinada
    return_source_documents=True,
    chain_type="refine",
    combine_docs_chain_kwargs={
        "question_prompt": question_prompt,
        "refine_prompt": refine_prompt,
        "document_variable_name": "context",
    },
)

# --- 5) Uso na prática ---
# Substitua a chamada obsoleta `chain.acall` por:
# response = await info_chain.arun({"question": user_message})
