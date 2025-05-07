from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationSummaryMemory
from constants import (
    LLM_MODEL,
    OLLAMA_URL,
    EMBEDDINGS_MODEL,
    PERSIST_DIR,
    PRICE_SYSTEM_PROMPT,
)

# LLM focado e determinístico
price_llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.0,
    streaming=False,
)

# Vectorstore trazendo só 3 trechos
price_emb = OllamaEmbeddings(model=EMBEDDINGS_MODEL, base_url=OLLAMA_URL)
price_vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=price_emb)
price_retriever = price_vectordb.as_retriever(search_kwargs={"k": 3})

# Memória resumida para manter o histórico enxuto (opcional para price; você pode usar buffer simples)
price_memory = ConversationSummaryMemory(
    llm=price_llm,
    memory_key="chat_history",
    output_key="answer",
    max_token_limit=800,
)

# Prompt “chat” para extração de preço
price_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        PRICE_SYSTEM_PROMPT
    ),
    HumanMessagePromptTemplate.from_template(
        "Responda **EXATAMENTE** o valor em reais, sem texto adicional."
        "Histórico da conversa:\n{chat_history}\n\n"
        "Catálogo de produtos:\n{context}\n\n"
        "Pergunta: Qual é o preço em reais do produto “{question}”?\n"
    ),
])

price_chain = ConversationalRetrievalChain.from_llm(
    llm=price_llm,
    retriever=price_retriever,
    memory=price_memory,
    return_source_documents=True,
    chain_type="stuff",
    combine_docs_chain_kwargs={"prompt": price_prompt}
)

