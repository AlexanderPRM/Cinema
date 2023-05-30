import uuid
import bson
import random


class MongoDocCreator:
    def gen_like_docs(self, film_id: uuid.UUID = None, user_id: uuid.UUID = None) -> dict:
        film_id = film_id or bson.Binary.from_uuid(uuid.uuid4())
        user_id = user_id or bson.Binary.from_uuid(uuid.uuid4())
        rating = random.randint(0, 10)

        return {
            "film_id": film_id,
            "user_id": user_id,
            "rating": rating,
        }

    def gen_ids(self, count: int) -> list:
        return [bson.Binary.from_uuid(uuid.uuid4()) for _ in range(count)]
