import pickle
import random

from tqdm import tqdm
from pymongo.database import Collection

from src.mongodb_manager import MongoManager
from src.docs_creator import MongoDocCreator
from core.settings import mongo_config, core_settings
from core.mongo_client import mongo_client


def get_data_from_file(file_path: str, count: int):
    mongo_dc = MongoDocCreator()
    data = list()
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
    except FileNotFoundError:
        data = mongo_dc.gen_ids(count)
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
    finally:
        return data


def get_film_id(film_list: list, film_count: int):
    start_film_id = random.randint(0, core_settings.film_count - film_count - 1)
    for i in range(start_film_id, start_film_id + film_count):
        yield film_list[i]


def load_data_to_db(collection_likes: Collection, film_ids: list, user_ids: list, batch_size: int):

    mongo_dc = MongoDocCreator()
    data_list = list()
    for i, user_id in enumerate(tqdm(user_ids)):
        users_liked_films = random.randint(
            core_settings.min_liked_films,
            core_settings.max_liked_films
        )
        temp_data = list()
        for film_id in get_film_id(film_list=film_ids, film_count=users_liked_films):
            temp_data.append(mongo_dc.gen_like_docs(user_id=user_id, film_id=film_id))
        data_list.extend(temp_data)
        if i % batch_size == 0:
            collection_likes.insert_many(data_list)
            data_list = list()
    if data_list:
        collection_likes.insert_many(data_list)


def main(mongo_client):
    mongo = MongoManager(client=mongo_client, db_name=mongo_config.db_name)

    collection_likes = mongo.create_collection(mongo_config.db_collection)

    film_ids = get_data_from_file(
        core_settings.film_ids_filename,
        core_settings.film_count
    )
    user_ids = get_data_from_file(
        core_settings.user_ids_filename,
        core_settings.user_count
    )

    load_data_to_db(collection_likes, film_ids, user_ids, core_settings.batch_size)


if __name__ == "__main__":
    main(mongo_client())
