from model.factory import ModelFactory
from classify.model import ClassifierModel
from classify.prompt import ClassifyPrompter
from langchain_core.runnables.base import RunnableSerializable
from typing import Dict, Literal

class ClassifyController():
    __classify_prompter: ClassifyPrompter
    __chain: RunnableSerializable

    def __init__(self):
        self.__classify_prompter = ClassifyPrompter()
        self.__chain: RunnableSerializable = self.__classify_prompter.get_templater() | ModelFactory.connect_factory(
            temperature=0.0, schema=ClassifierModel
        )

    async def get_response(self, input: str) ->  str:
        result = await self.__chain.ainvoke(input=input)
        return self.__process_response(msg=result.model_dump())

    def __process_response(self, msg: Dict[Literal['tag'], str]) -> str:
        return str(msg['tag']).lower()
