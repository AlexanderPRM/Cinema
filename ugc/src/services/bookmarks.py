from datetime import datetime
from http import HTTPStatus

from core.config import collections_names
from db.mongo import Mongo
from fastapi import HTTPException
from models.ugc_models import Bookmark


class BookmarksService:
    @staticmethod
    async def post_bookmark(mongodb: Mongo, user_id: str, film_id: str):
        collection = mongodb.get_collection(collections_names.BOOKMARK_COLLECTION)
        data = await collection.find_one({"user_id": user_id, "film_id": film_id})
        if data:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Bookmark already exists"
            )
        data = Bookmark(user_id=user_id, film_id=film_id, created_at=datetime.now())
        query_res = await collection.insert_one(data.dict())
        return query_res

    @staticmethod
    async def delete_bookmark(mongodb: Mongo, user_id: str, film_id: str):
        collection = mongodb.get_collection(collections_names.BOOKMARK_COLLECTION)
        data = await collection.find_one({"user_id": user_id, "film_id": film_id})
        if not data:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Bookmark doesnt exist")
        query_res = await collection.delete_one({"user_id": user_id, "film_id": film_id})
        return query_res

    @staticmethod
    async def get_bookmarks(mongodb: Mongo, user_id: str):
        collection = mongodb.get_collection(collections_names.BOOKMARK_COLLECTION)
        data = collection.find({"user_id": user_id})
        return [
            {"doc_id": str(entry["_id"]), "film_id": str(entry["film_id"])} async for entry in data
        ]
