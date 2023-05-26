from utils.models import Movie


class TransformToElasticView:
    def __init__(self, index: str) -> None:
        self.index = index

    def transform(self, movies: list[Movie]) -> list[dict]:
        actions = [
            {
                "_index": self.index,
                "_id": movie.id.__str__(),
                "_source": {
                    "id": movie.id.__str__(),
                    "imdb_rating": movie.rating,
                    "genre": [
                        {"id": genre["genre_id"], "name": genre["genre_name"]}
                        for genre in movie.genres
                    ],
                    "title": movie.title,
                    "description": movie.description,
                    "director": [
                        person["person_name"]
                        for person in movie.persons
                        if person["person_role"] == "director"
                    ],
                    "actors_names": [
                        person["person_name"]
                        for person in movie.persons
                        if person["person_role"] == "actor"
                    ],
                    "writers_names": [
                        person["person_name"]
                        for person in movie.persons
                        if person["person_role"] == "writer"
                    ],
                    "actors": [
                        {
                            "id": person["person_id"],
                            "name": person["person_name"],
                        }
                        for person in movie.persons
                        if person["person_role"] == "actor"
                    ],
                    "writers": [
                        {
                            "id": person["person_id"],
                            "name": person["person_name"],
                        }
                        for person in movie.persons
                        if person["person_role"] == "writer"
                    ],
                },
            }
            for movie in movies
        ]
        return actions
