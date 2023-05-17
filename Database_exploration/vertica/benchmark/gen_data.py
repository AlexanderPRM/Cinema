import uuid
import csv


def gen_data():
    n = 10000000
    lst = []
    file_50 = "data/films_progress_50.csv"
    file_1_000 = "data/films_progress_1_000.csv"
    file_10_000 = "data/films_progress_10_000.csv"
    file_100_000 = "data/films_progress_100_000.csv"
    file_1_000_000 = "data/films_progress_1_000_000.csv"
    file_10_000_000 = "data/films_progress_10_000_000.csv"

    for i in range(n):
        user_id = uuid.uuid4()
        movie_id = uuid.uuid4()
        timestamp = i

        dct = {"user_id": user_id, "movie_id": movie_id, "timestamp": timestamp}
        lst.append(dct)

    with open(file_50, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=lst[0].keys())
        writer.writeheader()
        for row in lst[:50]:
            writer.writerow(row)

    with open(file_1_000, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=lst[0].keys())
        writer.writeheader()
        for row in lst[:1000]:
            writer.writerow(row)

    with open(file_10_000, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=lst[0].keys())
        writer.writeheader()
        for row in lst[:10000]:
            writer.writerow(row)

    with open(file_100_000, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=lst[0].keys())
        writer.writeheader()
        for row in lst[:100000]:
            writer.writerow(row)

    with open(file_1_000_000, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=lst[0].keys())
        writer.writeheader()
        for row in lst[:1000000]:
            writer.writerow(row)

    with open(file_10_000_000, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=lst[0].keys())
        writer.writeheader()
        for row in lst:
            writer.writerow(row)


if __name__ == "__main__":
    gen_data()