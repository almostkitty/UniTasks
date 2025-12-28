FROM --platform=linux/amd64 python:3.13-slim

WORKDIR /app


RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir git+https://github.com/kurtmckee/feedparser.git

RUN pip install --no-cache-dir Flask==3.0.0 requests==2.31.0 gunicorn>=24.0.0

COPY services/ ./services/

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

RUN chmod +x services/news_parser/run.sh && \
    sed -i 's/\r$//' services/news_parser/run.sh

CMD ["sh", "/app/services/news_parser/run.sh"]

