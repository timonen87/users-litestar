# Базовый образ
FROM python:3.12-bookworm

# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl && \
    rm -rf /var/lib/apt/lists/*

    
# Устанавливаем Poetry (официальный метод)
ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION
ENV PATH="/root/.local/bin:$PATH"

# Настраиваем Poetry
RUN poetry config virtualenvs.create false

# Рабочая директория
WORKDIR /app

# Копируем зависимости отдельно для кэширования
COPY pyproject.toml poetry.lock ./

# Ставим зависимости (с явным указанием --no-cache)
RUN poetry install --only main --no-interaction --no-ansi --no-cache

# Копируем остальной код
COPY . .

# Переменные окружения
ENV PYTHONPATH=/app \
    PORT=8088

# Команда запуска
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8088", "app.asgi:app"]