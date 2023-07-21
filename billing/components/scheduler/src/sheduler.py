import json
import logging
import time
from uuid import uuid4

from core.config import config
from providers.base import Provider
from providers.yookassa_provider import get_yookassa


class Scheduler:
    def __init__(self, producer, auth_broker, notifications_broker, cache):
        self.producer = producer
        self.auth_broker = auth_broker
        self.notifications_broker = notifications_broker
        self.cache = cache
        self.provider: Provider = get_yookassa()

    async def get_previous_run_time(self):
        stored_data = self.cache.get("previous_run")
        if stored_data:
            return stored_data.decode("utf-8")
        return 0

    async def set_previous_run_time(self, previous_run_time):
        self.cache.set("previous_run", previous_run_time)

    async def taking_subs_away(self):
        previous_run_time = await self.get_previous_run_time()
        ended_subs = await self.producer.get_ended_subs(previous_run_time)
        logging.info(ended_subs)
        if ended_subs:
            for sub in ended_subs:
                sub = dict(sub)
                # disable subscription
                body = json.dumps(
                    {
                        "type_send": "subscribe_info",
                        "template_id": config.SUBSCRIBE_INFO_TEMPLATE_ID,
                        "notification_id": str(uuid4()),
                        "context": {
                            "users_id": [str(sub["user_id"])],
                            "payload": {"auto_renewal": sub["auto_renewal"]},
                        },
                    }
                )

                logging.info(body)
                # notification
                await self.notifications_broker.send_data(body)
                body = json.dumps(
                    {
                        "auto_renewal": sub["auto_renewal"],
                        "user_id": str(sub["user_id"]),
                    }
                )
                logging.info(body)
                # auth
                await self.auth_broker.send_data(body)

                if sub["auto_renewal"]:
                    cost = await self.producer.get_subscriprion_cost(
                        str(sub["subsciption_tier_id"])
                    )
                    currency = await self.producer.get_transaction_currency(
                        str(sub["transaction_id"])
                    )
                    # request to yookassa for auto-renewal
                    payment_data = {
                        "amount": {"value": cost["cost"], "currency": currency["currency"]},
                        "capture": True,
                        "payment_method_id": str(sub["transaction_id"]),
                        "description": f"Auto-Renewal "
                        f"subscription {str(sub['subsciption_tier_id'])}"
                        f"\nUser id: {str(sub['user_id'])}",
                    }
                    payment = self.provider.pay(payment_data=payment_data)
                    logging.info(
                        {
                            "payment.id": payment.id,
                            "payment.status": payment.status,
                            "paid": payment.paid,
                        }
                    )
        await self.set_previous_run_time(int(time.time()))
