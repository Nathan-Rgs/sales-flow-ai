from decouple import config
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from interface.model import ModelFactoryInterface
from pydantic import BaseModel

class LLMFactory(ModelFactoryInterface):

    @classmethod
    def connect_factory(cls, temperature: float, schema: BaseModel | None = None) -> BaseChatModel:
        return LLMFactory.__connect_cloud_gpt(temperature=temperature, schema=schema)

    @classmethod
    def __connect_local_ollama(cls, temperature: float, schema: BaseModel | None = None) -> ChatOllama:
        try:
            llm = ChatOllama(
                model=config(''),
                base_url=config(''),
                temperature=temperature,
                streaming=False
            )
            if schema == None: return llm
            return llm.with_structured_output(schema=schema)
        except Exception as e:
            raise e

    @classmethod
    def __connect_cloud_gpt(cls, temperature: float, schema: BaseModel | None = None) -> BaseChatModel:
        try:
            llm = ChatOpenAI(
                model=config("GPT_MODEL_NAME"),
                temperature=temperature,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=config('GPT_MODEL_API_KEY'),
                streaming=False
            )
            if schema == None: return llm
            return llm.with_structured_output(schema=schema)
        except Exception as e:
            raise e
