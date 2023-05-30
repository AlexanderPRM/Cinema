import logging

import backoff
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.consumer import AIOKafkaConsumer
from aiokafka.errors import KafkaTimeoutError, RequestTimedOutError, TooManyInFlightRequests
from aiokafka.producer import AIOKafkaProducer
from core.config import kafka_config
from db.base import BaseStorage


class Kafka(BaseStorage):
    def __init__(self, servers: list):
        self.servers = servers
        self.admin = AIOKafkaAdminClient(bootstrap_servers=servers)
        self.producer = AIOKafkaProducer(bootstrap_servers=servers)

    @backoff.on_exception(
        backoff.expo,
        (RequestTimedOutError, TooManyInFlightRequests, KafkaTimeoutError),
        max_time=30,
        max_tries=5,
    )
    async def create_topics_with_partitions(self, partitions, *topics):
        await self.admin.start()
        result = []
        topics_exists = set(await self.admin.list_topics())
        for topic in topics:
            if topic not in topics_exists:
                result.append(
                    NewTopic(
                        name=topic,
                        num_partitions=partitions,
                        replication_factor=1,
                    )
                )
        log = await self.admin.create_topics(result)
        logging.info(f"Topics create: {log}")
        await self.admin.close()

    @backoff.on_exception(
        backoff.expo,
        (RequestTimedOutError, TooManyInFlightRequests, KafkaTimeoutError),
        max_time=30,
        max_tries=5,
    )
    async def get_entries(self, topic, limit=float("inf")):
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.servers,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            group_id="get-events",
            consumer_timeout_ms=limit,
        )
        await consumer.start()
        result = []
        async for msg in consumer:
            result.append(
                {
                    "topic": msg.topic,
                    "partition": msg.partition,
                    "key": msg.key,
                    "value": msg.value,
                    "timestamp": msg.timestamp,
                }
            )
        await consumer.stop()
        return result

    async def save_entries(self, messages: list[dict]):
        for message in messages:
            await self.save_entry(
                topic=message["topic"],
                value=message["value"],
                key=message["key"],
            )
        logging.info(f"Success save {len(messages)} entries")

    @backoff.on_exception(
        backoff.expo,
        (RequestTimedOutError, TooManyInFlightRequests, KafkaTimeoutError),
        max_time=30,
        max_tries=5,
    )
    async def save_entry(self, topic, value, key):
        await self.producer.start()
        try:
            await self.producer.send(
                topic=topic, value=bytes(value, encoding="utf-8"), key=bytes(key, encoding="utf-8")
            )
        finally:
            await self.producer.stop()
        logging.info("Success save")


async def init_kafka():
    kafka = Kafka(kafka_config.BOOTSTRAP_SERVERS)
    await kafka.create_topics_with_partitions(12, "users_films")
    return kafka
