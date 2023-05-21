from time import sleep

from clickhouse_driver import Client
from settings import baseconfig

client = Client(host=baseconfig.client_host_1)
client_2 = Client(host=baseconfig.client_host_2)


def delete_from_all_shards():
    print("Clearing db ...")
    sleep(5)
    client.execute("ALTER TABLE shard.test DELETE WHERE timestamp >= 0;")
    client_2.execute("ALTER TABLE shard.test DELETE WHERE timestamp >= 0;")
    print("Clearing WELL!")
    sleep(5)
