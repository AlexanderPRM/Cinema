from clickhouse_driver import Client
from settings import baseconfig

client = Client(host=baseconfig.client_host_1)
client_2 = Client(host=baseconfig.client_host_2)

client.execute("CREATE DATABASE shard;")
client.execute(
    "CREATE TABLE shard.test (user_id String, movie_id String, timestamp UInt32) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/test', 'replica_1') ORDER BY (user_id, movie_id);"  # noqa: 402
)
client.execute(
    "CREATE TABLE default.test (user_id String, movie_id String, timestamp UInt32) ENGINE = Distributed('company_cluster', '', test, rand());"  # noqa:402
)
client_2.execute("CREATE DATABASE shard;")
client_2.execute(
    "CREATE TABLE shard.test (user_id String, movie_id String, timestamp UInt32) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_1') ORDER BY (user_id, movie_id);"  # noqa:402
)
client_2.execute(
    "CREATE TABLE default.test (user_id String, movie_id String, timestamp UInt32) ENGINE = Distributed('company_cluster', '', test, rand());"  # noqa:402
)
