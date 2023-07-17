import datetime
import json
import logging

from core.config import config
from yookassa import Configuration, Payment


class Scheduler:
    def __init__(self, producer, auth_broker, notifications_broker, cache):
        self.producer = producer
        self.auth_broker = auth_broker
        self.notifications_broker = notifications_broker
        self.cache = cache
        Configuration.account_id = config.YOOKASSA_SHOP_ID
        Configuration.secret_key = config.YOOKASSA_SECRET_KEY

    async def get_previous_run_time(self):
        stored_data = self.cache.get("previous_run")
        if stored_data:
            return stored_data.decode("utf-8")
        return "2000-07-12 20:15:04.883535"

    async def set_previous_run_time(self, previous_run_time):
        self.cache.set("previous_run", previous_run_time)

    async def taking_subs_away(self):
        # удалить
        # await self.set_previous_run_time("2000-07-12 20:15:04.883535")
        previous_run_time = datetime.datetime.strptime(
            (await self.get_previous_run_time()).split(".")[0], "%Y-%m-%d %H:%M:%S"
        )
        ended_subs = await self.producer.get_ended_subs(previous_run_time)
        await self.set_previous_run_time(str(datetime.datetime.now()))
        if ended_subs:
            for sub in ended_subs:
                sub = dict(sub)
                # disable subscription
                body = json.dumps(
                    {"user_id": str(sub["user_id"]), "subscribe_id": str(sub["subscribe_id"])}
                )
                logging.info(body)
                # notification
                await self.notifications_broker.send_data(body)
                body = json.dumps(
                    {
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
                    # request to yookassa for auto-renewal
                    payment = Payment.create(
                        {
                            "amount": {"value": cost["cost"], "currency": "RUB"},
                            "capture": True,
                            "payment_method_id": str(sub["transaction_id"]),
                            "description": f"Auto-Renewal subscription {str(sub['subsciption_tier_id'])} \n User id: {str(sub['user_id'])}",
                        }
                    )
                    logging.info(
                        {
                            "payment.id": payment.id,
                            "payment.status": payment.status,
                            "paid": payment.paid,
                        }
                    )
