from utils.models import Entry


class Transform:
    def transform(self, data: list[list]):
        data_to_save = []
        for entry in data:
            key = entry[0]
            value = entry[1]
            ids = key.split(";")
            movie_id = ids[1].split("=")[1]
            user_id = ids[0].split("=")[1]
            times = value.split("_")
            updated_at = times[1]
            timestamp=times[0]
            data_to_save.append(
                Entry(
                    movie_id=movie_id,
                    user_id=user_id,
                    updated_at=updated_at,
                    timestamp=timestamp,
                )
            )
        return data_to_save
