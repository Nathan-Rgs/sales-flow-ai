from abc import abstractmethod
from typing import Any

class EmbedderFactoryInterface():
    
    @abstractmethod
    def factory_embedder(cls) -> Any:
        raise NotImplementedError
