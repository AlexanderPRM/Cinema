import json

from core.config import postgres_settings
from services.providers_workers.base import BaseProviderWorker
from yookassa.domain.notification import WebhookNotification


class YooKassaProviderWorker(BaseProviderWorker):
    async def webhook_worker(self, request, psql):
        event_json = json.loads(request.body)
        notification_object = WebhookNotification(event_json)
        payment = notification_object.object
        if payment.status == "canceled":
            await psql.update_transaction_status_to_error(payment['id'])
            return
        # if payment.status == "succeeded":
        await psql.update_transaction_status_to_success(payment['id'])
        transaction = await psql.get_object_by_id(postgres_settings.TRANSACTIONS_LOG_TABLE, payment['id'])
        payment_details = json.loads(transaction['payment_details'])
        subscription_tiers = await psql.get_object_by_id(postgres_settings.SUBSCRIPTIONS_USERS_TABLE, payment_details['subscribe_tier_id'])
        await psql.create_subscription(transaction, payment_details, subscription_tiers)
        return


def get_yookassa_worker():
    return YooKassaProviderWorker()
