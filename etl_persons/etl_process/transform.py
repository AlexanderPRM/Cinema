class Transform:
    def transform(self, extracted_part: dict) -> list[dict]:
        transformed_part = []
        # print(extracted_part)
        for row in extracted_part:
            print(row["actors"])
            persons = {
                "id": row["id"],
                "full_name": row["full_name"],
                "director": [film for film in row["director"]],
                "actors": [film for film in row["actors"]],
                "writers": [film for film in row["writers"]],
            }
            transformed_part.append(persons)
        return transformed_part
