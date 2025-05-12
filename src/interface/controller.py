from abc import abstractmethod

class InfoController():

    @abstractmethod
    async def get_response(self, input: str, session_id: str) ->  str:
        raise NotImplementedError
