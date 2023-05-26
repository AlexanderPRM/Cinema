from app.quiries import INDEX_CREATE
from elasticsearch import Elasticsearch, helpers


class ElasticLoad:
    def __init__(self, conn: str, index) -> None:
        self.elastic: Elasticsearch = conn
        self.index = index
        try:
            self.elastic.indices.get(self.index)
        except Exception:
            self.elastic.indices.create(index=self.index, body=INDEX_CREATE)

    def load(self, movies: list[dict]) -> None:
        helpers.bulk(self.elastic, movies)
        self.elastic.indices.refresh(index=self.index)
