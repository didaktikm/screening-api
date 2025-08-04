FROM python:3.11-slim

# Установка системных зависимостей
RUN printf '\
deb http://mirror.yandex.ru/debian bookworm main contrib non-free\n\
deb http://mirror.yandex.ru/debian bookworm-updates main contrib non-free\n\
deb http://mirror.yandex.ru/debian-security bookworm-security main contrib non-free\n' \
    > /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

