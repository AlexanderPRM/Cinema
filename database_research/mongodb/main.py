import time
import random

from pymongo.database import Collection

from src.docs_creator import MongoDocCreator
from src.mongodb_manager import MongoManager
from core.logger import logger
from core.settings import mongo_config, core_settings
from core.mongo_client import mongo_client
from gen_data import get_data_from_file


def test_avg_film_rating(collection_likes: Collection, film_ids: list, avg_count: int = 100):
    avg_list = list()

    for _ in range(avg_count):
        film_id = random.choice(film_ids)

        start_time = time.time()
        _ = collection_likes.aggregate(
            [{"$match": {"film_id": film_id}}, {"$group": {"_id": None, "avg_value": {"$avg": "$rating"}}}]
        )
        response_time = time.time() - start_time

        avg_list.append(response_time)
    result = round((sum(avg_list) / avg_count) * 1000, 4)
    return result


def test_user_liked_films(collection_likes: Collection, user_ids: list, avg_count: int = 100, liked_min: int = core_settings.liked_min):
    avg_list = list()

    for _ in range(avg_count):
        user_id = random.choice(user_ids)

        start_time = time.time()
        collection_likes.find({"user_id": user_id, "rating": {"$gte": liked_min}})
        response_time = time.time() - start_time

        avg_list.append(response_time)

    result = round((sum(avg_list) / avg_count) * 1000, 4)
    return result


def test_load_doc(collection_likes: Collection, avg_count: int = 100):
    avg_list = list()
    mongo_dc = MongoDocCreator()

    for _ in range(avg_count):
        doc = mongo_dc.gen_like_docs()

        start_time = time.time()
        collection_likes.insert_one(doc)
        response_time = time.time() - start_time

        avg_list.append(response_time)

    result = round((sum(avg_list) / avg_count) * 1000, 4)
    return result


def main(mongo_client):
    mongo = MongoManager(client=mongo_client, db_name=mongo_config.db_name)

    collection_likes = mongo.get_collection(mongo_config.db_collection)

    film_ids = get_data_from_file(
        core_settings.film_ids_filename,
        core_settings.film_count
    )
    user_ids = get_data_from_file(
        core_settings.user_ids_filename,
        core_settings.user_count
    )
    for _ in range(10):
        time_1 = test_avg_film_rating(collection_likes=collection_likes, film_ids=film_ids)
        time_2 = test_user_liked_films(collection_likes=collection_likes, user_ids=user_ids)
        time_3 = test_load_doc(collection_likes=collection_likes)
        logger.info(f"avg_film_rating: {time_1}")
        logger.info(f"user_liked_film: {time_2}")
        logger.info(f"load_docs_in_ms: {time_3}")
        logger.info("=" * 23)


if __name__ == "__main__":
    main(mongo_client())
