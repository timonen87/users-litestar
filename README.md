# User CRUD API with Litestar and PostgreSQL

![Litestar](https://img.shields.io/badge/Litestar-2.x-blue)
![Python](https://img.shields.io/badge/Python-3.12-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)

REST API для управления пользователями с полным набором CRUD-операций, реализованный на фреймворке Litestar 2.x с использованием PostgreSQL.

## 🛠 Технологический стек

- **Backend**: 
  - Litestar 2.x (Python 3.12)
  - Advanced-SQLAlchemy (асинхронная работа с БД)
  - Uvicorn (ASGI-сервер)

- **База данных**: 
  - PostgreSQL 15
  - Asyncpg (драйвер)

- **Инфраструктура**:
  - Docker + Docker Compose
  - Poetry 1.8.3 (менеджер зависимостей)

- **Дополнительно**:
  - Msgspec (валидация данных)
  - Swagger UI (документация API)

## 🚀 Запуск проекта

### Предварительные требования
- Docker 20.10+
- Python 3.12
- Poetry 1.8.3

### Инструкция

1. Клонировать репозиторий:
```bash
git clone https://github.com/timonen87/user-litestar.git
cd users-litestar
```
2. Настроить окружение:
```bash
cp .env.example .env.dev
# Отредактировать .env.dev файл при необходимости ( .env.dev для Docker)
```
3. Запуск через Docker:
```bash
docker-compose up -d --build
```
4. Локальный запуск (без Docker):
```bash
poetry install
poetry run uvicorn app.asgi:app --host 0.0.0.0 --port 8088 --reload
```

После запуска API будет доступно по адресу:
http://localhost:8088/api/v1/users
Swagger документация: http://localhost:8088/schema/swagger

Пример запроса:
```bash
curl -X POST http://localhost:8088/api/v1users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "surname": "Doe", "password": "securepass123"}'

```

📂 Структура проекта
```bash
.
├── README.md
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── api.py
│   │       └── endpoints
│   │           ├── __init__.py
│   │           └── user_router.py
│   ├── asgi.py
│   ├── config.py
│   ├── db
│   │   ├── __init__.py
│   │   └── session.py
│   ├── deps
│   │   └── user_deps.py
│   ├── models
│   │   ├── __init__.py
│   │   └── user_model.py
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── base_repo.py
│   │   └── user_repo.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── user_schema.py
│   └── services
│       ├── __init__.py
│       ├── security.py
│       └── user_service.py
├── docker
│   └── Dockerfile
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── tests
│   └── __init__.py
└── users_litestar
    └── __init__.py

```