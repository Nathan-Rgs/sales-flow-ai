from decouple import config
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

class InfoEmbedderFactory():
    
    @classmethod
    def factory_embedder(cls) -> Embeddings:
        return InfoEmbedderFactory().__get_openai_embedder()

    @classmethod
    def __get_openai_embedder(cls) -> OpenAIEmbeddings:
        return OpenAIEmbeddings()
