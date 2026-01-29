FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Настройка Poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml ./

RUN poetry lock && poetry install --no-root --no-interaction

COPY . .

CMD alembic upgrade head && python -m src.main
