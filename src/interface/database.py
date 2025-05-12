from abc import abstractmethod
from typing import Any

class DatabaseInterface():

    @abstractmethod
    def connect_database() -> None:
        raise NotImplementedError

    @abstractmethod
    def init_retreiver() -> None:
        raise NotImplementedError

    @abstractmethod
    def get_retriver() -> Any:
        raise NotImplementedError
