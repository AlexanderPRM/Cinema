# Исследование ClickHouse
результаты представлены в /benchmark/chart.jpg и в /benchmark/output/load_benchmark_results.xlsx
## Запуск docker-compose

```sh
docker-compose --env-file config.env up --build
```

## Создание датасета films_progress.csv

```sh
docker exec -it clickhouse_python_1 python ./src/generate_data.py
```

## Создание БД и таблиц ClickHouse

```sh
docker exec -it clickhouse_python_1 python init_db.py
```

## Запуск тестирования

```sh
docker exec -it clickhouse_python_1 python main.py
```
