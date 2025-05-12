from utils.model import ModelFactory
from classify.model import ClassifierModel
from utils.prompt import PrompterFactory
from langchain_core.runnables.base import RunnableSerializable
from typing import Dict, Literal

class ClassifierController():
    __chain: RunnableSerializable

    def __init__(self):
        self.__chain: RunnableSerializable = PrompterFactory().factory_prompter() | ModelFactory.connect_factory(
            temperature=0.0, schema=ClassifierModel
        )

    async def get_response(self, input: str) ->  str:
        result = await self.__chain.ainvoke(input=input)
        return self.__process_response(msg=result.model_dump())

    def __process_response(self, msg: Dict[Literal['tag'], str]) -> str:
        return str(msg['tag']).lower()
