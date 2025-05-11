# rag/optimizeStrategy/indexing.py

import os
import logging
import shutil
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants import (
    API_KEY,
    EMBEDDINGS_MODEL,
    PERSIST_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    LLM_MODEL
)

logger = logging.getLogger(__name__)

def build_vectorstore(docs):
    """
    Chunka os docs, cria um FAISS vectorstore e persiste em disco.
    """
    # remove cache antigo (se existir)
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)

    # 1) Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    split_docs = splitter.split_documents(docs)

    # 2) Embeddings via OpenAI
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL, api_key=API_KEY)

    # 3) Cria o vectorstore FAISS
    vectordb = FAISS.from_documents(
        documents=split_docs,
        embedding=embeddings,
    )
    os.makedirs(PERSIST_DIR, exist_ok=True)
    vectordb.save_local(PERSIST_DIR)

    logger.info(f"Vectorstore criado com {vectordb.index.ntotal} vetores.")
    return vectordb

def load_vectorstore():
    """
    Carrega um FAISS vectorstore já persistido.
    """
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL, api_key=API_KEY)
    vectordb = FAISS.load_local(
        folder_path=PERSIST_DIR,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )
    logger.info(f"Vectorstore carregado com {vectordb.index.ntotal} vetores.")
    return vectordb

def get_vectorstore(docs):
    """
    Retorna um vectorstore:
    - Se já existe e tem vetores, carrega com load_vectorstore()
    - Senão, chama build_vectorstore(docs)
    """
    if os.path.exists(PERSIST_DIR):
        vectordb = load_vectorstore()
        if vectordb.index.ntotal > 0:
            return vectordb
        else:
            logger.info("Vectorstore vazio. Rebuildando…")
            return build_vectorstore(docs)
    else:
        logger.info("Vectorstore não encontrado. Criando novo…")
        return build_vectorstore(docs)
