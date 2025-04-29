from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from config import LLM_MODEL, OLLAMA_URL, EMBEDDINGS_MODEL, PERSIST_DIR, GENERIC_SYSTEM_PROMPT

# LLM e vectorstore
llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_URL, temperature=0.8, streaming=False)
emb = OllamaEmbeddings(model=EMBEDDINGS_MODEL, base_url=OLLAMA_URL)
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)

retriever = vectordb.as_retriever(search_kwargs={"k": 5})

# Prompt para preço
price_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Dado o contexto abaixo de catálogo de produtos, responda EXATAMENTE qual é o preço em reais do produto '{question}'.\nContexto:\n{context}\nResposta:\n"
    ),
])

price_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=None,
    return_source_documents=False,
    combine_docs_chain_kwargs={"prompt": price_prompt}
)
