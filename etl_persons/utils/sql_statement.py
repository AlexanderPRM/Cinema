STMT = """
    SELECT
        p.id,
        p.full_name,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'id', fw.id,
                    'title', fw.title
                )
            ) FILTER (WHERE pfw.role = 'director'),
            '[]'
        ) as director,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'id', fw.id,
                    'title', fw.title
                )
            ) FILTER (WHERE pfw.role = 'actor'),
            '[]'
        ) as actors,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'id', fw.id,
                    'title', fw.title
                )
            ) FILTER (WHERE pfw.role = 'writer'),
            '[]'
        ) as writers,
        MAX(p.updated_at) AS last_modified
    FROM
        content.person p
        LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
        LEFT JOIN content.film_work fw ON pfw.film_work_id = fw.id
    GROUP BY p.id
    """
