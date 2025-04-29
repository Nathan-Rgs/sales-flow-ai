from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from config import LLM_MODEL, OLLAMA_URL, EMBEDDINGS_MODEL, PERSIST_DIR, GENERIC_SYSTEM_PROMPT

llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_URL, temperature=0.7, streaming=False)
emb = OllamaEmbeddings(model=EMBEDDINGS_MODEL, base_url=OLLAMA_URL)
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)

retriever = vectordb.as_retriever(k=5)

rag_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "Resposta baseada no contexto e no histórico: \nContexto: {context}\nPergunta: {question}"
    ),
])

conv_rag = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=ConversationBufferMemory(),
    return_source_documents=False,
    combine_docs_chain_kwargs={"prompt": rag_prompt}
)
