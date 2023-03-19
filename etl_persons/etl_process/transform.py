from itertools import groupby


class Transform:
    def transform(self, extracted_part: dict) -> list[dict]:
        transformed_part = []
        for row in extracted_part:
            grouped_films = groupby(row["films"], lambda x: x["id"])
            films_with_roles = []
            for key, group in grouped_films:
                roles = [x["roles"] for x in group]
                films_with_roles.append({
                    "id": key,
                    "roles": roles
                })
            persons = {
                "id": row["id"],
                "full_name": row["full_name"],
                "films": films_with_roles,
            }
            transformed_part.append(persons)
        return transformed_part
