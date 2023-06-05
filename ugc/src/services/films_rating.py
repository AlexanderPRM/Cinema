from functools import lru_cache

from core.config import collections_names
from db.mongo import Mongo, get_db
from fastapi import Depends


class RatingService:
    def __init__(self, mongodb: Mongo = Depends(get_db)):
        self.collection = mongodb.get_collection(collections_names.FILM_RATING_COLLECTION)

    def update_rating(self, film_id, user_id, rating):
        self.collection.update_one(
            {"film_id": film_id, "user_id": user_id}, {"$set": {"rating": rating}}, upsert=True
        )
        return

    def delete_rating(self, film_id, user_id):
        self.collection.delete_one({"film_id": film_id, "user_id": user_id})
        return

    def check_rating_exists(self, film_id, user_id):
        result = self.collection.find({"film_id": film_id, "user_id": user_id})
        return list(result)

    def get_average_rating(self, film_id):
        result = self.collection.find({"film_id": film_id})
        ratings = [film["rating"] for film in result]
        average = sum(ratings) / len(ratings)
        return average


@lru_cache()
def get_rating_service(
    mongodb: Mongo = Depends(get_db),
) -> RatingService:
    return RatingService(mongodb)