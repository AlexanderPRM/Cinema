import asyncio
import time

from src.load_data_benchmark import load_data_benchmark, reed_data_benchmark
from src.remove_data import delete_from_all_shards

w_file = "./src/films_progress.csv"

loop = asyncio.get_event_loop()


if __name__ == "__main__":
    start_ts = time.time()
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=5000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=10000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=100000, w_file=w_file, batch=10000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=500000, w_file=w_file, batch=10000))
    loop.run_until_complete(reed_data_benchmark(count=500000, stress=False))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=1000000, w_file=w_file, batch=10000))
    loop.run_until_complete(reed_data_benchmark(count=1000000, stress=False))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=4000000, w_file=w_file, batch=10000))
    loop.run_until_complete(reed_data_benchmark(count=100000, stress=False))
    loop.run_until_complete(reed_data_benchmark(count=500000, stress=False))
    loop.run_until_complete(reed_data_benchmark(count=1000000, stress=False))
    loop.run_until_complete(reed_data_benchmark(count=2000000, stress=False))
    loop.run_until_complete(reed_data_benchmark(count=4000000, stress=False))
    delete_from_all_shards()

    loop.run_until_complete(load_data_benchmark(count=5000, w_file=w_file, batch=100000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=10000, w_file=w_file, batch=100000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=100000, w_file=w_file, batch=100000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=500000, w_file=w_file, batch=100000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=1000000, w_file=w_file, batch=100000))
    delete_from_all_shards()
    loop.run_until_complete(load_data_benchmark(count=4000000, w_file=w_file, batch=100000))
    tasks = [
        loop.create_task(reed_data_benchmark(count=3000000, stress=True)),
        loop.create_task(reed_data_benchmark(count=2000000, stress=True)),
        loop.create_task(reed_data_benchmark(count=4000000, stress=True)),
        loop.create_task(reed_data_benchmark(count=4000000, stress=True)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    end_ts = time.time()
    elapsed_time = end_ts - start_ts
    print(f"Global elapsed time {elapsed_time}")
    loop.close()
