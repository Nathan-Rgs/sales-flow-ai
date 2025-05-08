from classify.model import ClassifyModelFactory
from classify.prompt import ClassifyPrompter
from langchain_core.runnables.base import RunnableSerializable
from typing import Any, List

class ClassifyController():
    __classify_prompter: ClassifyPrompter
    __chain: Any

    def __init__(self):
        self.__classify_prompter = ClassifyPrompter()
        self.__chain: RunnableSerializable = self.__classify_prompter.get_templater() | ClassifyModelFactory.connect_factory(temperature=0.0)

    async def get_response(self, input: str) ->  str:
        result = await self.__chain.ainvoke(input=input)
        return self.__process_response(msg=result.content)

    def __process_response(self, msg: str) -> str:
        return str(msg).lower()
