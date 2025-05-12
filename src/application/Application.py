from classify.controller import ClassifyController
from common import get_tags
from info.controller import InfoController
from typing import List

class ApplicationRAG():

    __controller_classify: ClassifyController
    __controller_info: InfoController
    __tags = List[str]

    def __init__(self):
        self.__controller_classify = ClassifyController()
        self.__controller_info = InfoController()
        self.__tags = get_tags()

    async def run(self, input: str, session_id: str) -> str:
        if not self.__is_valid_input(input=input):
            raise Exception("Not Valid Input")
        tag = await self.__controller_classify.get_response(input=input)
        if tag == self.__tags[0]:
            ...
        elif tag == self.__tags[1]:
            return await self.__controller_info.get_response(input=input, session_id=session_id)
        elif tag == self.__tags[2]:
            ...
        else:
            ...
        return 'erro'

    def __is_valid_input(self, input: str) -> bool:
        if len(input) < 1:
            return False
        return True
