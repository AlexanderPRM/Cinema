# Исследование Vertica
результаты представлены на графике chart.jpg и в vertica.txt в директории benchmark
## Запуск docker-compose

```sh
docker-compose --env-file config.env up --build
```

## Создание dataset (нужно подождать, создание ~1gb данных)

```sh
docker exec -it vertica-python-1 python gen_data.py
```

## Запуск тестирования

```sh
docker exec -it vertica-python-1 python vertica.py
```

## Результаты тестирования

```sh
docker exec vertica-python-1 cat vertica.log
```