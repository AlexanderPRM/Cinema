# Инструкция по работе с проектом

## Документация Auth API

    https://app.swaggerhub.com/apis/AlexanderPRM/auth_api/1.0.0#/

    Также в папке auth_api лежит openapi.yaml
---
**Если вы собираетесь работать с Git, установите pre-commit hock**

    pre-commit install
---

**Создайте виртуальное окружение и войдите в него**

**(Linux\MacOS)**

    python3 -m venv venv
    source venv/bin/activate

---

### Настройте переменные окружения

Достаточно убрать расширение **.example** у файла **config.env.example**

**Если нужно, укажите свои значения**

    mv config.env.example config.env
---

### Для правильной работы сервиса Auth, нужно создать Google приложение

    Необходимо заменить этот файл или убрать расширение .example
    И внести свои данные из полученного файла при создании приложения

    ├── auth_api
        ├── src
            ├── google_client_secret.json.example

    Также в config.env есть настройка GOOGLE_FILE, там
    вы можете указать свой путь до нужного файла Google.

    Создать Google OAuth Client можно тут:
    https://console.cloud.google.com/apis/credentials
---

### Создайте сеть для Docker

    docker network create cinema

### Запустите docker-compose файлы

    docker-compose --env-file config.env up --build -d

    -- UGC сервис --
    docker-compose --env-file config.env -f ugc-mongo-cluster.yml up --build -d

    -- Сервис уведомлений --
    cd notifications
    docker-compose --env-file notf.env up --build -d

## Тесты

### Films_API

**Функциональные тесты**

#### Настройте переменные окружения для тестов Films API

    Уберите .example у файла config_tests.env.example и измените переменные, если нужно.

    ├── films_api
        ├── tests
            ├── functional
                ├── config_tests.env.example

#### Команда для запуска функциональных тестов Films API

    docker-compose -f films_api/tests/functional/docker-compose.yml --env-file films_api/tests/functional/config_tests.env up --build

#### Команда для запуска функциональных тестов Auth API

    docker-compose -f auth_api/tests/functional/docker-compose.yml --env-file config.env up --build

## Полезные команды*

**(Не через докер контейнер)**

---
**Создание суперюзера**

    flask --app auth_api/src/wsgi_run:run create-superuser

**Миграции**

    # Создание

    flask --app auth_api/src/wsgi_run:run db migrate -m "<comment>" --directory auth_api/migrations

    # Применение

    flask --app auth_api/src/wsgi_run:gunicorn_run db upgrade --directory auth_api/migrations

<br>

**(Через докер контейнер)**

---

    docker-compose exec auth_api

**Создание суперюзера**

    flask --app wsgi_run:run create-superuser

**Миграции**

    # Применение

    flask --app wsgi_run:run db upgrade

    # Создание

    !!!При разработке, миграции лучше создавать не через контейнер.

    flask --app wsgi_run:run db migrate -m "<comment>"
