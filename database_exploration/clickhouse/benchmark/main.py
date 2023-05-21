import asyncio
from time import sleep

from src.load_data_benchmark import load_data_benchmark
from src.remove_data import delete_from_all_shards

w_file = "./src/films_progress.csv"

loop = asyncio.get_event_loop()


if __name__ == "__main__":
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=5000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=10000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=100000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=500000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=1000000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=4000000, w_file=w_file, batch=10000))
    delete_from_all_shards()

    loop.run_until_complete(load_data_benchmark(count=5000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=10000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=100000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=500000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=1000000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=4000000, w_file=w_file, batch=10000))
    delete_from_all_shards()
