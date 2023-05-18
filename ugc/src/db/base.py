from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def get_entries():
        pass

    @abstractmethod
    def save_entry():
        pass

    @abstractmethod
    def save_entries():
        pass
