from abc import ABC, abstractmethod


class BaseProviderWorker(ABC):
    @abstractmethod
    def webhook_worker(self, request, psql):
        pass
