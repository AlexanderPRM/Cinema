import backoff
import elasticsearch.exceptions
from elasticsearch import helpers
from utils.connect import elastic_search_connection


class Load:
    def __init__(self, dsn, logger) -> None:
        self.dsn = dsn
        self.logger = logger
        self.create_index("persons")

    @backoff.on_exception(wait_gen=backoff.expo, exception=elasticsearch.exceptions.ConnectionError)
    def create_index(self, index_name: str) -> None:
        settings = {
            "refresh_interval": "1s",
            "analysis": {
                "filter": {
                    "english_stop": {"type": "stop", "stopwords": "_english_"},
                    "english_stemmer": {"type": "stemmer", "language": "english"},
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english",
                    },
                    "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                    "russian_stemmer": {"type": "stemmer", "language": "russian"},
                },
                "analyzer": {
                    "ru_en": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "english_stop",
                            "english_stemmer",
                            "english_possessive_stemmer",
                            "russian_stop",
                            "russian_stemmer",
                        ],
                    }
                },
            },
        }

        mappings = {
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "full_name": {
                    "type": "text",
                    "analyzer": "ru_en",
                    "fields": {"raw": {"type": "keyword"}},
                },
                "director": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "title": {"type": "text", "analyzer": "ru_en"},
                    },
                },
                "actor": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "title": {"type": "text", "analyzer": "ru_en"},
                    },
                },
                "writer": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "title": {"type": "text", "analyzer": "ru_en"},
                    },
                },
            },
        }

        with elastic_search_connection(self.dsn) as es:
            if not es.ping():
                raise elasticsearch.exceptions.ConnectionError
            if not es.indices.exists(index="persons"):
                es.indices.create(index=index_name, settings=settings, mappings=mappings)
                self.logger.info("Index created")

    def load(self, data: list[dict]) -> None:
        actions = [
            {
                "_index": "persons",
                "_id": row["id"],
                "_source": row,
            }
            for row in data
        ]
        with elastic_search_connection(self.dsn) as es:
            if not es.ping():
                raise elasticsearch.exceptions.ConnectionError
            helpers.bulk(es, actions)
            self.logger.info("Loaded {0} lines".format(len(data)))
