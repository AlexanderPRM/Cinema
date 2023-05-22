# Исследование ClickHouse
Тестирование (от начала и до конца) длится примерно **5 минут**  
Результаты будут представлены в Excel файле /benchmark/output/benchmark_results.xlsx  
Примерный вид вывода - /benchmark/write.jpg и /benchmark/reed.jpg  
## Иструкция по запуску тестирования
### Запуск docker-compose

```sh
docker-compose --env-file config.env up --build
```

### Создание датасета films_progress.csv

```sh
docker exec -it clickhouse_python_1 python ./src/generate_data.py
```

### Создание БД и таблиц ClickHouse

```sh
docker exec -it clickhouse_python_1 python init_db.py
```

### Запуск тестирования

```sh
docker exec -it clickhouse_python_1 python main.py
```
