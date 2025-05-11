from decouple import config
from info.embedding import InfoEmbedder
from langchain_chroma.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_core.retrievers import BaseRetriever

class InfoRetreiver():

    __db: VectorStore
    __retriver: BaseRetriever

    def factory_connect_database(self) -> None:
        self.__db = Chroma(
            persist_directory=config('DATABASE_FOLDER_PATH'),
            embedding_function=InfoEmbedder().get_embedder()
        )

    def factory_retreiver(self) -> None:
        self.__retriver =  self.__db.as_retriever()

    def get_retriver(self) -> BaseRetriever:
        return self.__retriver
