from http import HTTPStatus
from datetime import datetime

from fastapi import HTTPException

from db.mongo import Mongo
from models.models import Bookmark
from core.config import collections_names


class BookmarksService:
    @staticmethod
    def post_bookmark(mongodb: Mongo, user_id: str, film_id: str):
        collection = mongodb.get_collection(collections_names.BOOKMARK_COLLECTION)
        data = collection.find_one({"user_id": user_id, "film_id": film_id})
        if data:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Bookmark already exists"
            )
        data = Bookmark(user_id=user_id, film_id=film_id, created_at=datetime.now())
        collection.insert_one(data.dict())
        return data

    @staticmethod
    def delete_bookmark(mongodb: Mongo, user_id: str, film_id: str):
        collection = mongodb.get_collection(collections_names.BOOKMARK_COLLECTION)
        data = collection.find_one({"user_id": user_id, "film_id": film_id})
        if not data:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Bookmark doesnt exist")
        collection.delete_one({"user_id": user_id, "film_id": film_id})
