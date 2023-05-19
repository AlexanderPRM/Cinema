# Исследование ClickHouse
результаты представлены на графике chart_1.jpg и в load_data_benchmark.txt
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
