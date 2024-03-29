# Онлайн-кинотеатр

[![linters](https://github.com/AlexanderPRM/Async_API/actions/workflows/linters.yml/badge.svg)](https://github.com/AlexanderPRM/Async_API/actions/workflows/linters.yml)
![closed_issues](https://img.shields.io/github/issues-closed/AlexanderPRM/Cinema)
![commits/month](https://img.shields.io/github/commit-activity/m/AlexanderPRM/Cinema)
![repo-size](https://img.shields.io/github/repo-size/AlexanderPRM/Cinema)
![top-language](https://img.shields.io/github/languages/top/AlexanderPRM/Cinema)

![watchers](https://img.shields.io/github/watchers/AlexanderPRM/Cinema?style=social)
![forks](https://img.shields.io/github/forks/AlexanderPRM/Cinema?style=social)
![start](https://img.shields.io/github/stars/AlexanderPRM/Cinema?style=social)

---

[**Инструкция по запуску здесь**](https://github.com/AlexanderPRM/Cinema/blob/main/start_instruction.md)

Данный проект **Cinema** разбит на микросервисы, которые в совокупности
образуют полноценный онлайн-кинотеатр.

В проект входят такие сервисы как:

- Авторизация пользователей (auth_api)
- API для работы с фильмами, жанрами и персонами (films_api)
- Три ETL процесса которые отдельно перегружают персон, жанры и фильмы
из PostgreSQL в ElasticSearch для работы films_api с постоянно обновляющимися данными.
- Сервис который отслеживает просмотр фильма пользователем и позволяет
ему продолжить с места остановки (ugc)
- ETL процесс который перегружает события просмотров фильмов пользователями из Kafka в ClickHouse, для дальнейшей работы аналитиков.
- Сервис уведомлений который обрабатывает некоторые события из других микросервисов и события созданные администратором в админ-панели посылая письма пользователям с возможностью расширения на другие типы уведомлений.
  - В папке **notifications** вы можете увидеть архитектуру.

**films_api** и **auth_api** обрабатывают запросы через Nginx.

---
## Технологии используемые в проекте

Фреймворки:

- FastAPI, Flask, Django

Авторизация:

- JWT, OAuth2.0

Хранилища:

- SQLite, PostgreSQL, ElasticSearch, Redis, Kafka, ClickHouse, RabbitMQ

Контейнеренизация:

- Docker, Docker-Compose

Веб-сервера\Прокси:

- Gunicorn, Uvicorn, Nginx

---
### Разработчики

1. Пермяков Александр (Team Lead)
1. Денис Димитриев (Backend-разработчик)
1. Алексей Шаповалов (Backend-разработчик)
