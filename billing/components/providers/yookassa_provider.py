from core.config import config
from providers.base import Provider
from yookassa import Configuration, Payment, Refund, Settings
from yookassa.domain.exceptions.bad_request_error import BadRequestError


class YooKassa(Provider):
    def __init__(self, shop_id, secret_key: str = None, oauth_token: str = None) -> None:
        if secret_key:
            self.configuration = Configuration.configure(shop_id, secret_key)
        elif oauth_token:
            self.configuration = Configuration.configure_auth_token(oauth_token)

    def settings_info(self):
        return Settings.get_account_settings()

    def refund(self, refund_data: dict, idempotence_key):
        return Refund.create(refund_data, idempotence_key)

    def pay(self, payment_data: dict, idempotence_key=None):
        try:
            if idempotence_key:
                pay_info = Payment.create(payment_data, idempotence_key)
            else:
                pay_info = Payment.create(payment_data)
            return pay_info
        except BadRequestError as error:
            if error.args[0]["parameter"] == "Idempotence-Key":
                return
            raise error

    def payment_cancel(self, payment_id: int | str, idempotence_key: str):
        return Payment.cancel(payment_id, idempotence_key)

    def payment_capture(self, payment_id: int | str, data: dict, idempotence_key: str):
        return Payment.capture(payment_id, data, idempotence_key)

    def get_payment_info(self, payment_id: int | str):
        return Payment.find_one(payment_id)

    def get_refund_info(self, refund_id: int | str):
        return Refund.find_one(refund_id)

    def get_payments(self, data: dict = None):
        return Payment.list(data)

    def get_refunds(self, data: dict = None):
        return Refund.list(data)


def get_yookassa() -> YooKassa:
    return YooKassa(config.YOOKASSA_SHOP_ID, config.YOOKASSA_SHOP_SECRET)
