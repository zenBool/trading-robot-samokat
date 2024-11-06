# trading-robot/Dockerfile

# Используем базовый образ с Debian Bookworm
FROM python:3.12.7-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Копируем файлы проекта
COPY ./trading_bot /app/trading_bot/

# Устанавливаем зависимости через Poetry
# RUN /root/.local/bin/poetry install --no-root
# RUN poetry install --no-root
# RUN ls -la trading-bot
WORKDIR /app/trading_bot
