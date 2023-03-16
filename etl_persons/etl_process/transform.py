class Transform:
    def transform(self, extracted_part: dict) -> list[dict]:
        transformed_part = []
        for row in extracted_part:
            persons = {
                "id": row["id"],
                "full_name": row["full_name"],
                "films": [film for film in row["films"]],
            }
            transformed_part.append(persons)
        return transformed_part
