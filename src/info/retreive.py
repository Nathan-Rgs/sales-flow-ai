from decouple import config
from info.embedding import InfoEmbedderFactory
from langchain_chroma.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_core.retrievers import BaseRetriever

class InfoRetreiver():

    __db: VectorStore
    __retriver: BaseRetriever

    def connect_database(self) -> None:
        self.__db = Chroma(
            persist_directory=config('DATABASE_FOLDER_PATH'),
            embedding_function=InfoEmbedderFactory().factory_embedder()
        )

    def init_retreiver(self) -> None:
        self.__retriver =  self.__db.as_retriever()

    def get_retriver(self) -> VectorStoreRetriever:
        return self.__retriver
