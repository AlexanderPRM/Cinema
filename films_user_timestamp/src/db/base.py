from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):
    @abstractmethod
    def get_entries(self) -> Any:
        pass

    @abstractmethod
    def save_entry(self) -> Any:
        pass

    @abstractmethod
    def save_entries(self) -> Any:
        pass
