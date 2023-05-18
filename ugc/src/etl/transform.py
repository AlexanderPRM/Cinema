from etl.utils.models import Entry


class Transform:
    def transform(self, data: list[list]):
        data_to_save = []
        for entry in data:
            key = entry[0]
            value = entry[1]
            data_to_save.append(
                Entry(
                    movie_id=key.split(";")[1].split("=")[1],
                    user_id=key.split(";")[0].split("=")[1],
                    updated_at=value.split("_")[1],
                    timestamp=value.split("_")[0],
                )
            )
        return data_to_save
