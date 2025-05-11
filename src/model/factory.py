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
                model=config(''),
                base_url=config(''),
                temperature=temperature,
                streaming=False
            )
        except Exception as e:
            raise e

    @classmethod
    def __connect_cloud_gpt(cls, temperature: float) -> BaseChatModel:
        try:
            return ChatOpenAI(
                model=config("GPT_MODEL_NAME"),
                temperature=temperature,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=config('GPT_MODEL_API_KEY'),
                streaming=False
            )
        except Exception as e:
            raise e
