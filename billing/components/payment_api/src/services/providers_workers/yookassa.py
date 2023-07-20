import json

from services.providers_workers.base import BaseProviderWorker
from yookassa.domain.notification import WebhookNotification


class YooKassaProviderWorker(BaseProviderWorker):
    def webhook_worker(self, request, psql):
        event_json = json.loads(request.body)
        notification_object = WebhookNotification(event_json)
        payment = notification_object.object
        if payment.status == "canceled":
            psql.update_transaction_status_to_error(payment["id"])
            return
        # if payment.status == "succeeded":
        psql.update_transaction_status_to_success(payment["id"])
        psql.create_subscription(payment)
        return


def get_yookassa_worker():
    return YooKassaProviderWorker()
