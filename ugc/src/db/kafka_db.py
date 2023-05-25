import logging

import backoff
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

from core.config import kafka_config
from db.base import BaseStorage


class Kafka(BaseStorage):
    def __init__(self, servers: list):
        self.servers = servers
        self.admin = KafkaAdminClient(bootstrap_servers=servers)
        self.producer = KafkaProducer(bootstrap_servers=servers)

    @backoff.backoff(backoff.expo, max_time=30, max_tries=5)
    def create_topics_with_partitions(self, partitions, *topics):
        result = []
        topics_exists = set(self.admin.list_topics())
        for topic in topics:
            if topic not in topics_exists:
                result.append(
                    NewTopic(
                        name=topic,
                        num_partitions=partitions,
                        replication_factor=1,
                    )
                )
        logging.info(self.admin.create_topics(result))

    @backoff.backoff(backoff.expo, max_time=30, max_tries=5)
    def get_entries(self, topic, limit=float("inf")):
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.servers,
            auto_offset_reset="earliest",
            group_id="get-events",
            consumer_timeout_ms=limit,
        )
        result = []
        for msg in consumer:
            result.append(
                {
                    "topic": msg.topic,
                    "partition": msg.partition,
                    "key": msg.key,
                    "value": msg.value,
                    "timestamp": msg.timestamp,
                }
            )
        return result

    def save_entries(self, messages: list[dict]):
        for message in messages:
            self.save_entry(
                topic=message["topic"],
                value=message["value"],
                key=message["key"],
            )

    @backoff.backoff(backoff.expo, max_time=30, max_tries=5)
    def save_entry(self, topic, value, key):
        self.producer.send(
            topic=topic, value=bytes(value, encoding="utf-8"), key=bytes(key, encoding="utf-8")
        )
        self.producer.flush()
        return "OK"


def init_kafka():
    kafka = Kafka(kafka_config.BOOTSTRAP_SERVERS)
    kafka.create_topics_with_partitions(12, "users_films")
    return kafka
