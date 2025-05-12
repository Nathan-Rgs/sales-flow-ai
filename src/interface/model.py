from abc import abstractmethod
from typing import Any

class ModelFactoryInterface():

    @abstractmethod
    def connect_factory(cls, temperature: float, schema: Any | None = None) -> Any:
        raise NotImplementedError
