# Исследование MongoDB
Результаты представлены на графике chart.jpg и в results.txt
## Запуск docker-compose

```sh
docker-compose --env-file config.env up --build
```

## Настройка кластера MongoDB

```sh
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
```
```sh
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
```
```sh
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
```
```sh
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
```
```sh
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
```
```sh
docker exec -it mongos2 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
```
```sh
docker exec -it mongos2 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
```

## Генерация данных и их загрузка в бд

```sh
docker exec -it mongodb-python-1 python gen_data.py
```

## Создание индексов

```sh
docker exec -it mongodb-python-1 python create_index.py
```

## Запуск тестирования

```sh
docker exec -it mongodb-python-1 python main.py
```

## Результаты

```sh
docker exec mongodb-python-1 cat mongodb.log
```