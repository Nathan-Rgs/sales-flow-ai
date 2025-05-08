from decouple import config
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from interface.model import ModelInterface

class ModelFactory(ModelInterface):

    @classmethod
    def connect_factory(cls, temperature: float) -> BaseChatModel:
        return ModelFactory.__connect_cloud_gpt(temperature=temperature)

    @classmethod
    def __connect_local_ollama(cls, temperature: float) -> ChatOllama:
        try:
            return ChatOllama(
                model=config('ollama_model_name'),
                base_url=config('local_url_ollama'),
                temperature=temperature,
                streaming=False
            )
        except Exception as e:
            raise e

    @classmethod
    def __connect_cloud_gpt(cls, temperature: float) -> BaseChatModel:
        try:
            return ChatOpenAI(
                model=config("gpt_model_name"),
                temperature=temperature,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=config('gpt_model_api_key'),
                streaming=False
            )
        except Exception as e:
            raise e
