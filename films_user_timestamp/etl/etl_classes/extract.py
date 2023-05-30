import uuid
from datetime import datetime


class Extract:
    def __init__(self, db, limit: int, state) -> None:
        self.db = db
        self.limit = limit
        self.state = state

    async def extract(self):
        data = await self.db.get_entries(topic="users_films", limit=1000)
        data_list = []
        for entry in data:
            key = entry["key"].decode("utf-8")
            value = entry["value"].decode("utf-8")
            updated_at = datetime.strptime(value.split("_")[1], "%Y-%m-%d %H:%M:%S.%f")
            last_updated = await self.state.get_state("last_updated")
            if (
                last_updated is None
                or datetime.strptime(
                    await self.state.get_state("last_updated").decode("utf-8"),
                    "%Y-%m-%d %H:%M:%S.%f",
                )
                < updated_at
            ):
                await self.state.set_state("last_updated", value.split("_")[1])
                data_list.append([key, value])
            if len(data_list) == self.limit or data[-1] == entry:
                yield data_list
                data_list = []

    async def gen_data(self):
        n = 100
        lst = []

        for i in range(n):
            key = "user_id=" + str(uuid.uuid4()) + ";" + "movie_id=" + str(uuid.uuid4())
            value = f"{i}:{i}:{i}" + "_" + str(datetime.now())

            dct = {"key": key, "value": value, "topic": "users_films"}
            lst.append(dct)
            await self.db.save_entry(topic="users_films", value=value, key=key)
