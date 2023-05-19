from load_data_benchmark import load_data_benchmark
from time import sleep
from remove_data import delete_from_all_shards
import asyncio

w_file = "films_progress.csv"

loop = asyncio.get_event_loop()


if __name__ == "__main__":
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(50, w_file))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(1000, w_file))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(10000, w_file))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(100000, w_file))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(1000000, w_file))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(10000000, w_file))
    sleep(5)
    loop.run_until_complete(load_data_benchmark(50, w_file))
    loop.run_until_complete(load_data_benchmark(1000, w_file))
    loop.run_until_complete(load_data_benchmark(10000, w_file))
    loop.run_until_complete(load_data_benchmark(100000, w_file))
    loop.run_until_complete(load_data_benchmark(1000000, w_file))
    delete_from_all_shards()
