INDEX_CREATE = {
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
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
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "imdb_rating": {"type": "float"},
            "genre": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "title": {"type": "text", "analyzer": "ru_en", "fields": {"raw": {"type": "keyword"}}},
            "description": {"type": "text", "analyzer": "ru_en"},
            "director": {"type": "text", "analyzer": "ru_en"},
            "actors_names": {"type": "text", "analyzer": "ru_en"},
            "writers_names": {"type": "text", "analyzer": "ru_en"},
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
        },
    },
}

SQL_QUERY = """
    SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating,
        fw.type,
        fw.created_at,
        fw.updated_at,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'person_role', pfw.role,
                    'person_id', p.id,
                    'person_name', p.full_name,
                    'updated_at', p.updated_at
                )
            ) FILTER (WHERE p.id is not null),
            '[]'
        ) as persons,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'genre_id', g.id,
                    'genre_name', g.name
                )
            ) FILTER (WHERE g.id is not null),
            '[]'
        ) as genres,
        array_agg(g.updated_at) as g_updated_at,
        array_agg(p.updated_at) as p_updated_at
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    %s
    GROUP BY fw.id
    ORDER BY fw.updated_at
    LIMIT %s;
    """
