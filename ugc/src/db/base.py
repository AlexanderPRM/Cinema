from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def get_entry():
        pass

    @abstractmethod
    def get_entries():
        pass

    @abstractmethod
    def save_entry():
        pass

    @abstractmethod
    def save_entries():
        pass
