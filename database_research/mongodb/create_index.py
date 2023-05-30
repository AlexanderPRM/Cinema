from core.mongo_client import mongo_client
from core.settings import mongo_config
from src.mongodb_manager import MongoManager


def main(mongo_client):
    mongo = MongoManager(client=mongo_client, db_name=mongo_config.db_name)

    collection_likes = mongo.get_collection(mongo_config.db_collection)

    collection_likes.create_index([("film_id", 1)])
    collection_likes.create_index([("user_id", 1)])


if __name__ == "__main__":
    main(mongo_client())
