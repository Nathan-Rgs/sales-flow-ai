from logging import getLogger, Logger
from utils.common import get_tags
from typing import List
import controller

class ApplicationRAG():

    __controller_classifier: controller.ClassifierController
    __controller_price: controller.PriceController
    __controller_info: controller.InfoController
    __controller_smalltalk: controller.SmalltalkController
    __tags = List[str]
    __logger: Logger

    def __init__(self):
        self.__logger = getLogger('root')
        self.__controller_classifier = controller.ClassifierController()
        self.__controller_price = controller.PriceController()
        self.__controller_info = controller.InfoController()
        self.__controller_smalltalk = controller.SmalltalkController()
        self.__tags = get_tags()

    async def run(self, input: str, session_id: str) -> str:
        self.__logger.info("Received user prompt")
        result: str | None = None
        if not self.__is_valid_input(input=input):
            raise Exception("Not Valid Input")
        tag = await self.__controller_classifier.get_response(input=input)
        if tag == self.__tags[0]:
            result = await self.__controller_price.get_response(input=input, session_id=session_id)
        elif tag == self.__tags[1]:
            result = await self.__controller_info.get_response(input=input, session_id=session_id)
        elif tag == self.__tags[2]:
            result = await self.__controller_smalltalk.get_response(input=input, session_id=session_id)
        else:
            self.__logger.info("Something get wrong in generating response for user")
            return 'erro'
        self.__logger.info("Sending response for user prompt")
        return str(result)

    def __is_valid_input(self, input: str) -> bool:
        if len(input) < 1:
            return False
        return True
