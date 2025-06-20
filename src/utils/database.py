from decouple import config
from utils.embedding import EmbedderFactory
from langchain_chroma.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_core.retrievers import BaseRetriever
from interface.database import DatabaseInterface

class Database(DatabaseInterface):

    __db: VectorStore
    __retriver: BaseRetriever

    def connect_database(self) -> None:
        self.__db = self.__connect_faiss()

    def init_retreiver(self) -> None:
        self.__retriver =  self.__db.as_retriever()

    def get_retriver(self) -> VectorStoreRetriever:
        return self.__retriver

    def __connect_chroma(self) -> Chroma:
        return Chroma(
            persist_directory=config('DATABASE_FOLDER_PATH'),
            embedding_function=EmbedderFactory().factory_embedder()
        )

    def __connect_faiss(self) -> Chroma:
        return FAISS.load_local(
            folder_path=config('DATABASE_FOLDER_PATH'),
            embeddings=EmbedderFactory().factory_embedder(),
            allow_dangerous_deserialization=True,
        )
