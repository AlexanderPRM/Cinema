from abc import ABC, abstractmethod


class BaseProviderWorker(ABC):
    @abstractmethod
    async def webhook_worker(self, request, psql):
        pass

    @abstractmethod
    async def update_subscription_status(self, payment_info, psql):
        pass
