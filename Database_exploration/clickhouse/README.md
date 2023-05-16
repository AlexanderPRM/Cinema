# Исследование по ClickHouse

## Запуск docker-compose

```sh
docker-compose --env-file config.env up --build
```

## Создание датасета films_progress.csv

```sh
docker exec -it clickhouse_python_1 python generate_data.py
```

## Создание БД и таблиц ClickHouse

```sh
docker exec -it clickhouse_python_1 python init_db.py
```

## Запуск тестирования

```sh
docker exec -it clickhouse_python_1 python main.py
```
