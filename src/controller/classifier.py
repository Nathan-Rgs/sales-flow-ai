from utils.model import ModelFactory
from model.classifier import ClassifierModel
from utils.prompt import PrompterFactory
from interface.controller import InfoControllerInterface
from langchain_core.runnables.base import RunnableSerializable
from logging import getLogger, Logger
from typing import Dict, Literal

class ClassifierController(InfoControllerInterface):
    __chain: RunnableSerializable
    __logger: Logger

    def __init__(self):
        self.__logger = getLogger('root')
        self.__chain: RunnableSerializable = PrompterFactory().factory_prompter() | ModelFactory.connect_factory(
            temperature=0.0, schema=ClassifierModel
        )

    async def get_response(self, input: str) ->  str:
        self.__logger.info("Invoking response from Classifier Chain")
        result = await self.__chain.ainvoke(input=input)
        return self.__process_response(msg=result.model_dump())

    def __process_response(self, msg: Dict[Literal['tag'], str]) -> str:
        self.__logger.info("Processing response from Classifier Chain")
        return str(msg['tag']).lower()
