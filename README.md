# Проектная работа 4 спринта: Async API

[![linters](https://github.com/AlexanderPRM/Async_API/actions/workflows/linters.yml/badge.svg)](https://github.com/AlexanderPRM/Async_API/actions/workflows/linters.yml)

## Инструкция по настройке проекта

### Создайте виртуальное окружение

#### (Linux\MacOS)

    python3 -m venv venv
    source venv/bin/activate

### Установите зависимости

##### (Для работы с API)

    pip install -r requirements.txt

##### (Для работы с ETL)

    pip install -r etl_genres/requirements.txt
    pip install -r etl_persons/requirements.txt
    pip install -r etl_movies/requirements.txt

##### (Инструменты разработки)

    pip install -r requirements_dev.txt

### Настройте переменные окружения

#### Достаточно убрать расширение .example у файла config.env.example.

#### Если нужно, укажите свои значения

    mv config.env.example config.env

### Если вы собираетесь работать с Git, установите pre-commit hock

    pre-commit install

### Запустите docker-compose

    docker-compose --env-file config.env up --build
