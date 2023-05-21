import csv
import time

from clickhouse_driver import Client
from settings import baseconfig

client = Client(host=baseconfig.client_host_1)
client_2 = Client(host=baseconfig.client_host_2)


async def write_to_ch(data):
    query = "INSERT INTO default.test (user_id, movie_id, timestamp) VALUES "
    values = ",".join(
        [
            "('{}','{}','{}')".format(
                str(d.get("user_id")), str(d.get("movie_id")), d.get("timestamp")
            )
            for d in data
        ]
    )
    query_full = query + values
    client.execute(query_full)


async def load_data_benchmark(count, w_file):
    with open(w_file, mode="r") as file:
        reader = csv.DictReader(file)
        lst = []
        cnt = 0
        n = 1000000
        start_ts = time.time()
        for row in reader:
            cnt += 1
            if cnt > count:
                break
            lst.append(row)
            if len(lst) == n:
                print(f"{cnt} writing: " + str(len(lst)))
                await write_to_ch(data=lst)
                lst = []
        if lst != []:
            print(f"!{cnt} writing: " + str(len(lst)))
            await write_to_ch(data=lst)

    end_ts = time.time()
    elapsed_time = end_ts - start_ts
    shard_1 = client.execute("SELECT COUNT(*) as count FROM shard.test;")
    shard_2 = client_2.execute("SELECT COUNT(*) as count FROM shard.test;")
    shard_1 = shard_1[0][0]
    shard_2 = shard_2[0][0]
    print("Time elapsed: {} seconds".format(elapsed_time))

    with open("load_data_benchmark.txt", "a") as file:
        file.write(
            f"load data in ClickHouse ({count}):"
            + f"{str(elapsed_time)};\nShard 1: {shard_1} || Shard 2: {shard_2}\n"
        )
