# Проектная работа 4 спринта: Async API

[![linters](https://github.com/AlexanderPRM/Async_API/actions/workflows/linters.yml/badge.svg)](https://github.com/AlexanderPRM/Async_API/actions/workflows/linters.yml)

## Инструкция по настройке проекта*

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

## Тесты

### Функциональные тесты*

#### Настройте переменные окружения для тестов

    Уберите .example у файла config_tests.env.example и измените переменные, если нужно.

    ├── tests
        ├── functional
            ├── config_tests.env.example

#### Команда для запуска функциональных тестов

    docker-compose -f tests/functional/docker-compose.yml --env-file tests/functional/config_tests.env up --build

## Полезные команды*

### Не через докер контейнер. (Если прокинуты порты у БД)

<br>

**Создание суперюзера**

    flask --app auth_api/src/wsgi_run:run create-superuser

**Миграции**

    # Создание

    flask --app auth_api/src/wsgi_run:run db migrate -m "<comment>" --directory auth_api/migrations

    # Применение

    flask --app auth_api/src/wsgi_run:gunicorn_run db upgrade --directory auth_api/migrations

<br>

### Через докер контейнер

    docker-compose exec auth_api

**Создание суперюзера**

    flask --app wsgi_run:run create-superuser

**Миграции**

    # Применение

    flask --app wsgi_run:run db upgrade

    # Создание

    При разработке, миграции создавать не через контейнер.
