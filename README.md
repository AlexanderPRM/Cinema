# Онлайн-кинотеатр

[![linters](https://github.com/AlexanderPRM/Async_API/actions/workflows/linters.yml/badge.svg)](https://github.com/AlexanderPRM/Async_API/actions/workflows/linters.yml)

[**Инструкция по запуску здесь**](https://github.com/AlexanderPRM/Cinema/blob/main/start_instruction.md)

Данные проект **Cinema** разбит на микросервисы, которые в совокупности
образуют полноценный онлайн-кинотеатр.

В проект входят такие сервисы как:

- Авторизация пользователей (auth_api)
- API для работы с фильмами, жанрами и персонами (films_api)
- Три ETL процесса которые отдельно перегружают персон, жанры и фильмы
из PostgreSQL в ElasticSearch для работы films_api с постоянно обновляющимися данными.
- Сервис который отслеживает просмотр фильма пользователем и позволяет
ему продолжить с места остановки (ugc)

**films_api** и **auth_api** обрабатывают запросы через Nginx.

## Технологии используемые в проекте

Фреймворки:

- FastAPI, Flask

Авторизация:

- JWT, OAuth2.0

Хранилища:

- SQLite, PostgreSQL, ElasticSearch, Redis, Kafka, ClickHouse

Контейнеренизация:

- Docker, Docker-Compose

Веб-сервера\Прокси:

- Gunicorn, Uvicorn, Nginx
