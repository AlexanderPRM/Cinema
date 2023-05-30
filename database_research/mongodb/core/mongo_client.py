from pymongo import MongoClient

from .settings import mongo_config


client = MongoClient(
    f'{mongo_config.host_1}:{mongo_config.port}, {mongo_config.host_2}:{mongo_config.port}'
)


def mongo_client() -> MongoClient:
    return client
