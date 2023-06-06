from functools import lru_cache

import pymongo
from core.config import collections_names
from db.mongo import Mongo, get_db
from fastapi import Depends


class ReviewService:
    def __init__(self, mongodb: Mongo = Depends(get_db)):
        self.collection = mongodb.get_collection(collections_names.FILM_REVIEW_COLLECTION)

    def get_reviews_list(self, film_id, sort_direction, page_number, page_size):
        if sort_direction == "desc":
            reviews = (
                self.collection.find({"film_id": film_id})
                .sort("created_at", pymongo.DESCENDING)
                .skip((page_number - 1) * page_size)
                .limit(page_size)
            )  # По убыванию
        elif sort_direction == "asc":
            reviews = (
                self.collection.find({"film_id": film_id})
                .sort("created_at")
                .skip((page_number - 1) * page_size)
                .limit(page_size)
            )  # По возрастанию
        return reviews


@lru_cache()
def get_review_service(
    mongodb: Mongo = Depends(get_db),
) -> ReviewService:
    return ReviewService(mongodb)
