import csv
import uuid


def gen_data():
    n = 10000000
    lst = []
    w_file = "films_progress.csv"

    for i in range(n):
        user_id = uuid.uuid4()
        movie_id = uuid.uuid4()
        timestamp = i

        dct = {"user_id": user_id, "movie_id": movie_id, "timestamp": timestamp}
        lst.append(dct)

    with open(w_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=lst[0].keys())
        writer.writeheader()
        for row in lst:
            writer.writerow(row)
