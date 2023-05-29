# Исследование ClickHouse
Тестирование (от начала и до конца) длится примерно **5 минут**  
Результаты будут представлены в Excel файле /benchmark/output/benchmark_results.xlsx  
Примерный вид вывода - /benchmark/write.jpg и /benchmark/reed.jpg  

В рамках исследования мы измеряли скорость записи и чтения данных в/из ClickHouse под нагрузкой и без неё.  
Сравнили скорость записи данных при разных батчах (10к и 100к записей)  
Максимальное кол-во данных = 4 млн записей вида (user_id: str, movie_id: str, timestamp: int)  
Скорость на графиках (speed) измеряется в [кол-во записей/сек]
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
