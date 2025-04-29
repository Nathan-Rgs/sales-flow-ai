from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config import (
    LLM_MODEL,
    OLLAMA_URL,
    EMBEDDINGS_MODEL,
    PERSIST_DIR,
    GENERIC_SYSTEM_PROMPT,
)

# 1) inicializa o LLM, embeddings e vectorstore (sem filtros)
llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_URL, temperature=0.8, streaming=False)
emb = OllamaEmbeddings(model=EMBEDDINGS_MODEL, base_url=OLLAMA_URL)
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)

# 2) retriever “cru” — busca sem metadata filters
retriever = vectordb.as_retriever(k=5)

# 3) memória para manter o fluxo da conversa
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 4) prompt combinado com seu system prompt genérico
info_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Abaixo há informações úteis do nosso conhecimento.\n"
        "Contexto: {context}\n"
        "Pergunta: {question}"
    ),
])

# 5) monta a ConversationalRetrievalChain sem filtros adicionais
info_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=None,
    return_source_documents=False,
    combine_docs_chain_kwargs={"prompt": info_prompt},
)
