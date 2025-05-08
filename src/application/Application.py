from classify.controller import ClassifyController
from decouple import config
from typing import List

class ApplicationRAG():
    __responser_classify: ClassifyController
    __tags = List[str]

    def __init__(self):
        self.__responser_classify = ClassifyController()
        self.__tags = self.__get_tags()
        print(self.__tags)

    async def run(self, input: str) -> str:
        if not self.__is_valid_input(input=input):
            raise Exception("Not Valid Input")
        tag = await self.__responser_classify.get_response(input=input)
        if tag == self.__tags[0]:
            ...
        elif tag == self.__tags[1]:
            ...
        elif tag == self.__tags[2]:
            ...
        else:
            ...
        return tag

    def __get_response() -> str:
        ...

    def __is_valid_input(self, input: str) -> bool:
        if len(input) < 1:
            return False
        return True

    def __get_tags(self) -> List[str]:
        tags: str = config('tags')
        return tags.lower().split(sep=', ')
