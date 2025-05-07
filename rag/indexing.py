# rag/optmizeStrategy/indexing.py

import os
import logging
import shutil
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants import (
    EMBEDDINGS_MODEL,
    OLLAMA_URL,
    PERSIST_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

logger = logging.getLogger(__name__)

def build_vectorstore(docs):
    """
    Chunka os docs, cria um Chroma vectorstore e persiste em disco.
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

    # 2) Embeddings
    embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL, base_url=OLLAMA_URL)

    # 3) Cria e persiste o vectorstore
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    vectordb.persist()
    logger.info(f"Vectorstore criado com {vectordb._collection.count()} vetores.")
    return vectordb

def load_vectorstore():
    """
    Carrega um Chroma vectorstore já persistido.
    """
    embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL, base_url=OLLAMA_URL)
    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
    )
    logger.info(f"Vectorstore carregado com {vectordb._collection.count()} vetores.")
    return vectordb

def get_vectorstore(docs):
    """
    Retorna um vectorstore:
    - Se já existe e tem vetores, carrega com load_vectorstore()
    - Senão, chama build_vectorstore(docs)
    """
    if os.path.exists(PERSIST_DIR):
        vectordb = load_vectorstore()
        if vectordb._collection.count() > 0:
            return vectordb
        else:
            logger.info("Vectorstore vazio. Rebuildando…")
            return build_vectorstore(docs)
    else:
        logger.info("Vectorstore não encontrado. Criando novo…")
        return build_vectorstore(docs)
