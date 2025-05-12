from abc import abstractmethod
from typing import Any

class PrompterFactoryInterface():        

    @abstractmethod
    def factory_prompter(cls, system_msg: str, human_msg: str) -> Any:
        raise NotImplementedError
