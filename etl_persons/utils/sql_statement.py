STMT = """
    SELECT
        p.id,
        p.full_name,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'id', fw.id,
                    'roles', pfw.role
                )
            ) FILTER (WHERE pfw.role IS NOT NULL ),
            '[]'
        ) as films,
        MAX(p.updated_at) AS last_modified
    FROM
        content.person p
        LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
        LEFT JOIN content.film_work fw ON pfw.film_work_id = fw.id
    GROUP BY p.id
    """
