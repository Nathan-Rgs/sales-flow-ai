from decouple import config
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

class InfoEmbedder():
    def __init__(self):
        ...
    
    @classmethod
    def get_embedder(cls) -> Embeddings:
        return InfoEmbedder().__get_openai_embedder()

    @classmethod
    def __get_openai_embedder(cls) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            model=config('GPT_MODEL_NAME'),
            api_key=config('GPT_MODEL_API_KEY')
        )
