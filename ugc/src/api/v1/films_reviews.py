from datetime import datetime, timedelta
from http import HTTPStatus
from uuid import UUID

from bson.objectid import ObjectId
from core.config import CommonQueryParams, collections_names
from core.jwt import JWTBearer
from core.logging_setup import LOGGER
from db.mongo import Mongo, get_db
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.exceptions import HTTPException
from models.ugc_models import FilmReview, Review, SortDirectionEnum
from services.films_reviews import ReviewService, get_review_service

router = APIRouter()


@router.get("/", status_code=HTTPStatus.OK)
async def get_all_fresh_reviews(
    auth: dict = Depends(JWTBearer()), mongodb: Mongo = Depends(get_db)
):
    if auth["role"] != "superuser":
        raise HTTPException(detail="Token Invalid", status_code=HTTPStatus.FORBIDDEN)
    collection = mongodb.get_collection(collections_names.FILM_REVIEW_LIKES)
    week_ago = datetime.now() - timedelta(weeks=1)
    query = collection.find(
        {
            "$and": [
                {"$where": "this.likes > this.notified_likes"},
                {"updated_at": {"$gt": week_ago}},
            ]
        }
    )
    data = []
    async for entry in query:
        data.append(
            {
                "review_id": str(entry["review_id"]),
                "likes": entry["likes"],
                "notified_likes": entry["notified_likes"],
                "updated_at": entry["updated_at"],
            }
        )
    collection.update_many({}, [{"$set": {"notified_likes": "$likes"}}])
    return {"message": "Success", "data": data}


@router.get("/author/{review_id}", status_code=HTTPStatus.OK)
async def get_author_review(
    review_id: str, auth: dict = Depends(JWTBearer()), mongodb: Mongo = Depends(get_db)
):
    if auth["role"] != "superuser":
        raise HTTPException(detail="Token Invalid", status_code=HTTPStatus.FORBIDDEN)
    collection = mongodb.get_collection(collections_names.FILM_REVIEW_COLLECTION)
    query = await collection.find_one({"_id": ObjectId(review_id)})
    return {"author": query["author"] if query else None}


@router.get("/last_liked/{review_id}", status_code=HTTPStatus.OK)
async def get_user_last_liked_review(
    review_id: str, auth: dict = Depends(JWTBearer()), mongodb: Mongo = Depends(get_db)
):
    if auth["role"] != "superuser":
        raise HTTPException(detail="Token Invalid", status_code=HTTPStatus.FORBIDDEN)
    review_rate_collection = mongodb.get_collection(collections_names.FILM_REVIEW_RATE_COLLECTION)
    query = review_rate_collection.find({"review_id": ObjectId(review_id)}).sort("_id", -1)
    list_query = await query.to_list(length=1)
    last_liker = list_query[0]["user_id"] if list_query else None
    return {"Last liked by user": last_liker}


@router.post(
    "/{film_id}",
    response_description="Добавление рецензии к фильму",
    summary="Рецензия",
    status_code=HTTPStatus.CREATED,
)
async def film_review(
    film_id: UUID,
    body: FilmReview,
    auth: dict = Depends(JWTBearer()),
    mongodb: Mongo = Depends(get_db),
):
    collection = mongodb.get_collection(collections_names.FILM_REVIEW_COLLECTION)
    doc = {
        "film_id": film_id.__str__(),
        "author": auth["user_id"].__str__(),
        "text": body.text,
        "created_at": datetime.now(),
    }
    query_res = await collection.insert_one(doc)
    likes_collection = mongodb.get_collection(collections_names.FILM_REVIEW_LIKES)
    likes_doc = {
        "review_id": query_res.inserted_id,
        "likes": 0,
        "notified_likes": 0,
        "updated_at": datetime.now(),
        "created_at": datetime.now(),
    }
    await likes_collection.insert_one(likes_doc)
    LOGGER.info(f"Succesfully insert film review {query_res.inserted_id}")
    return {"message": "Success", "_id": str(query_res.inserted_id)}


@router.post(
    "/rate/{review_id}",
    response_description="Оценка рецензии",
    summary="Оценка",
    status_code=HTTPStatus.CREATED,
)
async def film_review_rate(
    review_id: str = Path(..., description="ReviewID is not Correct", regex=r"^[0-9a-f]{24}$"),
    rate: int = Body(embed=True, ge=1, le=10),
    auth: dict = Depends(JWTBearer()),
    mongodb: Mongo = Depends(get_db),
):
    review_id = ObjectId(review_id)

    review_collection = mongodb.get_collection(collections_names.FILM_REVIEW_COLLECTION)
    if not await review_collection.find_one({"_id": review_id}):
        raise HTTPException(
            detail="This review does not exist", status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    review_rate_collection = mongodb.get_collection(collections_names.FILM_REVIEW_RATE_COLLECTION)
    if await review_rate_collection.find_one({"review_id": review_id, "user_id": auth["user_id"]}):
        raise HTTPException(
            detail="User already rate this review", status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    res = await review_rate_collection.insert_one(
        {"review_id": review_id, "user_id": auth["user_id"].__str__(), "rate": rate}
    )
    review_likes = mongodb.get_collection(collections_names.FILM_REVIEW_LIKES)
    await review_likes.update_one({"review_id": review_id}, {"$inc": {"likes": 1}})
    LOGGER.info(f"New rate {rate} for review {review_id}")
    return {"message": "Success", "_id": str(res.inserted_id)}


@router.put(
    "/rate/{rate_id}",
    response_description="Изменение оценки рецензии",
    summary="Оценка",
    status_code=HTTPStatus.CREATED,
)
async def film_review_rate_update(
    rate_id: str = Path(..., description="ReviewID is not Correct", regex=r"^[0-9a-f]{24}$"),
    new_rate: int = Body(embed=True, ge=1, le=10),
    auth: dict = Depends(JWTBearer()),
    mongodb: Mongo = Depends(get_db),
):
    rate_id = ObjectId(rate_id)
    review_rate_collection = mongodb.get_collection(collections_names.FILM_REVIEW_RATE_COLLECTION)
    res = await review_rate_collection.find_one_and_update(
        {"_id": rate_id}, {"$set": {"rate": new_rate}}, return_document=True
    )
    if not res:
        raise HTTPException(
            detail="Rate does not exists", status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )
    LOGGER.info(f"Updated rate {new_rate} for review {rate_id}")
    return {"message": "Success", "_id": str(res["_id"])}


@router.get(
    "/{film_id}",
    response_description="Получение списка рецензий всех пользователей",
    summary="Рецензия",
    status_code=HTTPStatus.OK,
)
async def film_get_reviews(
    film_id: UUID,
    review_service: ReviewService = Depends(get_review_service),
    auth: dict = Depends(JWTBearer()),
    sort_direction: SortDirectionEnum = Query(...),
    commons: CommonQueryParams = Depends(CommonQueryParams),
):
    reviews = await review_service.get_reviews_list(
        film_id=film_id.__str__(),
        sort_direction=sort_direction,
        page_number=commons.page_number,
        page_size=commons.page_size,
    )
    response = [
        Review(
            id=str(review["_id"]),
            film_id=review["film_id"],
            author=review["author"],
            text=review["text"],
            created_at=str(review["created_at"]),
        )
        async for review in reviews
    ]
    return {"reviews": response}
