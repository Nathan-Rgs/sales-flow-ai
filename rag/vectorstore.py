
from loaders import load_documents
from indexing import get_vectorstore
from constants import DOCS_PATH

_docs = load_documents(DOCS_PATH)
vectordb = get_vectorstore(_docs)
retriever = vectordb.as_retriever()
