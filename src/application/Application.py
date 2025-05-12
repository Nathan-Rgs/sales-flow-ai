from classify.controller import ClassifierController
from utils.common import get_tags
from info.controller import InfoController
from price.controller import PriceController
from small_talk.controller import SmalltalkController
from typing import List

class ApplicationRAG():

    __controller_classifier: ClassifierController
    __controller_price: PriceController
    __controller_info: InfoController
    __controller_smalltalk: SmalltalkController
    __tags = List[str]

    def __init__(self):
        self.__controller_classifier = ClassifierController()
        self.__controller_price = PriceController()
        self.__controller_info = InfoController()
        self.__controller_smalltalk = SmalltalkController()
        self.__tags = get_tags()

    async def run(self, input: str, session_id: str) -> str:
        if not self.__is_valid_input(input=input):
            raise Exception("Not Valid Input")
        tag = await self.__controller_classifier.get_response(input=input)
        if tag == self.__tags[0]:
            return await self.__controller_price.get_response(input=input, session_id=session_id)
        elif tag == self.__tags[1]:
            return await self.__controller_info.get_response(input=input, session_id=session_id)
        elif tag == self.__tags[2]:
            return await self.__controller_smalltalk.get_response(input=input, session_id=session_id)
        else:
            ...
        return 'erro'

    def __is_valid_input(self, input: str) -> bool:
        if len(input) < 1:
            return False
        return True
