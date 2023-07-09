from abc import ABC, abstractmethod


class Provider(ABC):
    @abstractmethod
    def pay(self, *args, **kwargs):
        pass

    @abstractmethod
    def refund(self, *args, **kwargs):
        pass

    @abstractmethod
    def payment_cancel(self, *args, **kwargs):
        pass

    @abstractmethod
    def payment_capture(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_payment_info(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_refund_info(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_payments(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_refunds(self, *args, **kwargs):
        pass
