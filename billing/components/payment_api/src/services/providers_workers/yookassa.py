import json

from core.config import postgres_settings
from db.postgres import PostgreSQL
from fastapi import Request
from services.providers_workers.base import BaseProviderWorker
from yookassa.domain.notification import PaymentResponse, WebhookNotification


class YooKassaProviderWorker(BaseProviderWorker):
    async def webhook_worker(self, request: Request, psql: PostgreSQL):
        event_json = json.loads(await request.body())
        notification_object = WebhookNotification(event_json)
        payment = notification_object.object
        if notification_object.event == "payment.succeeded":
            transaction = await psql.get_object_by_id(
                postgres_settings.TRANSACTIONS_LOG_TABLE, payment.id
            )
            if transaction.operate_status == "waiting":
                _, payment_details, subscription_tiers = await self.__update_or_create_subscription(
                    psql, transaction
                )
                await psql.update_transaction_status_to_success(payment.id)
                return {
                    "user_id": str(transaction.user_id),
                    "ttl": subscription_tiers.duration,
                    "auto_renewal": payment_details.auto_renewal,
                }
            return None
        elif notification_object.event == "payment.canceled":
            await psql.update_transaction_status_to_canceled(payment.id)
            return None
        elif notification_object.event == "refund.succeeded":
            transaction = await psql.get_object_by_id(
                postgres_settings.TRANSACTIONS_LOG_TABLE, payment.payment_id
            )
            await psql.deactivate_subscribe(str(transaction.user_id))
            return None
        else:
            raise ValueError("Unknown event status")

    async def update_subscription_status(
        self,
        transaction,
        payment_info: PaymentResponse,
        psql: PostgreSQL,
    ):
        if payment_info.status == "succeeded" and transaction.operate_status == "waiting":
            _, _, _ = await self.__update_or_create_subscription(psql, transaction)
            await psql.update_transaction_status_to_success(payment_info.id)
            return transaction
        return None

    async def __update_or_create_subscription(self, psql: PostgreSQL, transaction):
        payment_details = transaction.payment_details
        subscription_tiers = await psql.get_object_by_id(
            postgres_settings.SUBSCRIPTIONS_TABLE, payment_details["subscribe_tier_id"]
        )
        subscription = await psql.get_subscription_by_user_id(transaction.user_id)
        if subscription:
            await psql.update_subscription(transaction, payment_details, subscription_tiers)
        else:
            await psql.create_subscription(transaction, payment_details, subscription_tiers)
        return transaction, payment_details, subscription_tiers


def get_yookassa_worker():
    return YooKassaProviderWorker()
