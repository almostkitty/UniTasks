FROM --platform=linux/amd64 python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir Flask==3.0.0 requests==2.31.0 gunicorn>=24.0.0

COPY services/ ./services/

ENV PYTHONUNBUFFERED=1
ENV PORT=8080


RUN chmod +x services/categorizer/run.sh && \
    sed -i 's/\r$//' services/categorizer/run.sh

# Скрипт для поддержки динамического PORT от Yandex Cloud
CMD ["sh", "/app/services/categorizer/run.sh"]

